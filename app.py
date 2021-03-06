#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from time import localtime, strftime, strptime
from datetime import date, timedelta
from functools import wraps
from email_module import mail

from glob_var import *
import sqlite3, os, re, hashlib




######## initializaton ########

app = Flask(__name__)
app.secret_key = 's\x1f}\xc8\xe29c\x84\xd1\x87P\x8e\xa5h5s\xf1\xfff\xcf\xfcK\xe8i'

######## user utils ########
def verify(id, passwd, admin_type):
    with sqlite3.connect(DATABASE) as database:
        cursor = database.execute("SELECT PASSWORD FROM %s WHERE ID = ? "%admin_type, (id,))
        correct = cursor.fetchone()
        if correct == None:  # wrong id
            flash("用户名不存在！", category="error")
            return False
        else:  # correct id
            hashed_pass = hashlib.sha256((passwd+SALT+id).encode('utf-8')).hexdigest()
            if hashed_pass == correct[0]:
                return True    # correct id-pass pair
            else:  # wrong passwd
                flash("密码错误！", category="error")
                return False

def adminRegist(id, passwd, admin_type):
    '''Register a new administrater.

    admin_type should be either 'admin1' or 'admin2'.
    '''
    if admin_type == 'admin1':
        db = 'ADMIN'
    elif admin_type == 'admin2':
        db = 'ADMIN2'
    else:
        flash("注册信息错误", category='error')
    if id == '' or passwd == '':
        flash("用户名或密码不能为空！", category='error')
        return False
    with sqlite3.connect(DATABASE) as database:
        cursor = database.execute("select password from %s where id = ? "%db, (id,))
        empty = cursor.fetchone()
        if empty != None:
            flash("用户名已经存在!", category='warning')
            return False
        else:  # id is new
            treated = hashlib.sha256((passwd+SALT+id).encode('utf-8'))
            sql_sentence = "insert into %s (id, password) values (?, ?)"%db
            cur = database.execute(sql_sentence,(id, treated.hexdigest()))
            database.commit()
            flash("注册成功！<br>请登录！", category='success')
            return True

def printLog(log):
    ''' Use to write log for user's behaviour '''
    with open(LOG, encoding="utf-8", mode='a') as f:
        f.write(log)
        f.write("operation time: {}\n\n".format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        print("ADD TO LOG")

def applying_material(form):
    ''' Use to dump the applying information into the database, using the request.form as argument.

    Return True, if the form is successfully added to database and the email is sent. Else, False is returned.'''
    mat_form = [
        (
            form['dep'], form['name'], form['material'], form['contact'],
            form['startyear'], form['startmonth'], form['startday'],
            form['starthour'], form['endingyear'], form['endingmonth'],
            form['endingday'], form['endinghour']
        )
    ]
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        try:
            c.executemany('INSERT INTO MATERIAL VALUES (NULL,?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, 0, NULL)', mat_form)
            database.commit()
            hint = "社联小伙伴{}，你好！\n你已成功提交物资借出申请，请勿重复提交!\n本邮件为自动发出，请勿回复。\n".format(form['name'])
        except:
            flash("申请提交失败，请重试或联系技术人员。", category="error")
            # 如果出现数据无法添加到数据库（可能由于检查合理性时未检查出的错误）
            return False
        else:
            if email_enable:
                result = mail(hint, [form['contact']])
                if not result: # 如果邮件发送出现问题
                    flash("邮件发送失败，请联系技术人员。", category="error")
                    return False
            return True


def applying_classroom(form):
    '''Very much the same as applying_material, except for it's used to dump data into table CLASSROOM'''
    mat_form = [
        (
            form['dep'], form['name'], form['classroom'], form['contact'],
            form['startyear'], form['startmonth'], form['startday'],
            form['starthour'], form['endingyear'], form['endingmonth'],
            form['endingday'], form['endinghour']
        )
    ]
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        try:
            c.executemany('INSERT INTO CLASSROOM VALUES (NULL,?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, 0, NULL)', mat_form)
            database.commit()
            hint = "社联小伙伴{}，你好！\n你已成功提交教室借出申请，请勿重复提交!\n本邮件为自动发出，请勿回复。\n".format(form['name'])
        except:
            flash("申请提交失败，请重试或联系技术人员。", category="error")
            # 如果出现数据无法添加到数据库（可能由于检查合理性时未检查出的错误）
            return False
        else:
            if email_enable:
                result = mail(hint, [form['contact']])
                if not result: # 如果邮件发送出现问题
                    flash("邮件发送失败，请联系技术人员。", category="error")
                    return False
            return True


def get_new_apply(tablename, status_code):
    '''
    Take the name of the table and status_code that is checked as the
    arguments, return the list of complete content of matching records. Items
    in the list are tuples.

    Tablename should be a string and status_code is expected to be integers 0, 1, 2.
    '''
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        cursor = c.execute('select * from %s where status = %d;'% (tablename, status_code)) # 这里不是binding，好像不能用？占位
        new_apply_list = cursor.fetchall()
        # fetchall() returns a list of  tuples
        return new_apply_list


def record_scrutiny_results(tablename, indx, status_code, admin):
    ''' Take the name of the table, index of application and the renewed status_code, name of admin as arguments, the function updates the status of application on demand.

    Note that under normal condition, status_code should be 1 (representing approval of application) or 2 (representing denial)'''
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        c.execute("update %s set STATUS = ? where ID = ? "%tablename , (status_code, indx)  )
        c.execute("update %s set ADMIN = ? where ID = ? "%tablename , (admin, indx)  )
        # 提取审批后的记录储存于info中用于发送邮件
        cursor = c.execute('select * from %s where ID = %d;'% (tablename, indx))
        info = cursor.fetchall()[0]
        database.commit()
        if status_code == 1:
            feedback = "社联小伙伴{}，你好！\n你提交的借用{}的申请已批准。\n借出时间：{}年{}月{}日 {}时,请在{}年{}月{}日 {}时之前归还。 \n本邮件为自动发出，请勿回复。\n".format(info[2], info[3],info[5],info[6],info[7],info[8],info[9],info[10],info[11],info[12])
        elif status_code == 2:
            feedback = "社联小伙伴{}，你好！\n很遗憾，你借用{}的申请未能通过！\n本邮件为自动发出，请勿回复。\n".format(info[2], info[3])
        if email_enable:
            result = mail(feedback, [info[4]])
            if not result: # 如果邮件发送出现问题
                flash("邮件发送失败，请联系技术人员。", category="error")


def expire_date():
    a_month = timedelta(days=31)
    expire_date = date.today() - a_month
    return expire_date

def get_records(tablename, year, month):
    ''' Take the name of the table and year, month that is checked as the arguments, return the list of complete content of matching (i.e. the ending time is later than the given one) records. Items in the list are tuples.

    Tablename should be a string and year, month is expected to be integers.
    '''
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        cursor = c.execute('select * from %s where endingyear >= %d and endingmonth >= %d;'% (tablename, year, month))
        records = cursor.fetchall()
        return records

def login_verify(to_be_decorated):
    '''  check-in decorator  '''
    @wraps(to_be_decorated)
    def decorated(*args, **kwargs):
        if 'id' not in session and 'id2' not in session:
            flash("请登录！", category="error")     # NOTE: flash-msg show in the NEXT page
            return redirect(url_for('login'))
        return to_be_decorated(*args, **kwargs)
    return decorated

        ##### 检查合法性 #####

#检查字符串中危险的特殊字符

def check_slashes(plain):   # `str` is python reserved keyword, DON'T use it
    slashes=['{','}','\'','\"','%','?','\\',',']
    for i in plain:
            if i in slashes:
                flash("输入中包含非法字符", category="error")
                return False
    return True


#检查邮箱格式
def email_available(email): #email: str 格式
    pattern = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    match = pattern.match(email)
    if match:
        return True
    else:
        flash("邮箱格式不正确！", category="error")
        return False


#检查姓名格式
def name_available(name):   # name: str 格式
    pattern = re.compile(r"[\u4e00-\u9fa5]{2,8}")   # 匹配2到8个汉字
    match = pattern.match(name)
    if match:
        return True
    else:
        flash("不是合法的姓名！", category="error")
        return False


def struct_timing(year, month, day, hour):
    '''
    Take **strings** or **integers** as arguments, return a struct_time instance if it
    represents time with given format, else return `None`
    '''
    a = [year, month, day, hour]
    for i in range(0, 4):
        if isinstance(a[i],int):
            a[i] = repr(a[i])
    try:
        struct_time1 = strptime(a[0] + ' ' + a[1] + ' ' + a[2] + ' ' + a[3],
                                '%Y %m %d %H')
        return struct_time1
    except ValueError:
        flash("请输入正确的时间信息！", category="error")
        return None
    except:
        flash("访问错误！", category="error")


def form_legitimate(dic, column):
    """Check the legitimacy of the request form.

    Column is either 'material' or 'classroom' """
    items_1 = ('name', 'contact', 'dep', column)
    time_1 = ('startyear', 'startmonth', 'startday', 'starthour')
    time_2 = ('endingyear', 'endingmonth', 'endingday',  'endinghour')
    try:
        for item in items_1:
            if not check_slashes(dic[item]):
                return False
        if not name_available(dic['name']) and email_available(dic['contact']):
            return False
            # keep me wondering why it's "and" instead of "or"
        start = [dic[x] for x in time_1]
        end = [dic[x] for x in time_2]
        t1 = struct_timing(*start)
        t2 = struct_timing(*end)
        if t1 == None or t2 == None:
            return False
        elif t2 <= t1 or t1 <= localtime():
            flash("请输入正确的时间信息！", category="error")
            return False
        return True
    except :
        flash('INVALID REQUEST', category='error')
        return False


######## views  ########
    ''' entry & exit '''
@app.route('/')
def index():
    return redirect(url_for('personal'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        #检查危险字符
        if check_slashes(request.form['id']) \
                and check_slashes(request.form['passwd']):
            session['passwd'] = request.form['passwd']
            if request.form['admin_type'] == 'admin1':
                session['id'] = request.form['id']
                if verify(session['id'], session['passwd'], 'ADMIN'):
                    try:
                        # don't carry your passwd with you
                        assert session.pop('passwd', None) != None
                    except:
                        session.pop('id', None)
                        return redirect(url_for('login'))
                    flash("着陆成功！", category='success')
                    return redirect(url_for('personal'))
                else:
                    session.pop('id', None)
                    session.pop('passwd', None)
                    return redirect(url_for('login'))
            elif request.form['admin_type'] == 'admin2':
                session['id2'] = request.form['id']
                if verify(session['id2'], session['passwd'], 'ADMIN2'):
                    try:
                        # don't carry your passwd with you
                        assert session.pop('passwd', None) != None
                    except:
                        session.pop('id2', None)
                        return redirect(url_for('login'))
                    flash("着陆成功！", category='success')
                    return redirect(url_for('personal'))
                else:
                    session.pop('id2', None)
                    session.pop('passwd', None)
                    return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route('/register/', methods=['POST'])
def register():
    id = request.form['id']
    passwd = request.form['passwd_first']
    if passwd != request.form['passwd_second']:
        flash("两次密码不相同！<br>换个好记一点的吧？", category='error')
        return redirect(url_for('login'))
    # elif len(passwd) < 8:
    #     flash("密码太短了！", category='warning')
    #     return redirect(url_for('login'))
    elif request.form['invitation'] != INVITATION:
        flash("邀请码错误！", category='error')
        return redirect(url_for('login'))
    else:
        if adminRegist(id, passwd, request.form['admin_type']):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route('/home/')
def personal():
    return render_template("home.html")

@app.route('/logout/')
def logout():
    # 已登陆的管理员才能看到logout按钮，否则报错
    assert 'id' in session or 'id2' in session
    if 'id' in session:
        # clear session
        session.pop('id', None) # about the usage of session.pop see: https://stackoverflow.com/questions/20115662/what-does-the-second-argument-of-the-session-pop-method-do-in-python-flask
    elif 'id2' in session:
        session.pop('id2', None)
    print(session.pop('passwd', None))  # should get `None`
    flash("已登出", category='message')
    return redirect(url_for('index'))

    ''' entry to modules '''

@app.route('/materials/', methods=['GET', 'POST'])
def materials_apply():
    if request.method == 'GET':
        return render_template('materials_apply.html')
    elif request.method == 'POST':
        #格式控制
        if form_legitimate(request.form, 'material'):
            if applying_material(request.form):
                # NOTE: should not exceed 79 chars (per line)
                printLog("user {} apply for material: {}\n".format(
                    request.form['name'], request.form['material']))
                flash("表格提交成功, 请检查相应邮箱（含垃圾箱）。", category='success')
            return redirect(url_for('personal'))
        else:
            return render_template('materials_apply.html')

@app.route('/classroom/', methods=['GET', 'POST'])
def classroom_apply():
    if request.method == 'GET':
        return render_template('classroom_apply.html')
    elif request.method == 'POST':
        if form_legitimate(request.form, 'classroom'):
            if applying_classroom(request.form):
                printLog("user {} apply for classroom: {}\n".format(
                    request.form['name'], request.form['classroom']))
                flash("表格提交成功, 请检查相应邮箱（含垃圾箱）。", category='success')
            return redirect(url_for('personal'))
        else:
            return render_template('classroom_apply.html')


@app.route('/classroom-usage/')
def classroom_usage():
    if request.method == 'GET':
        def get_endtime(record):
            return struct_timing(record[9], record[10], record[11], record[12])
        results = get_records('classroom', date.today().year, date.today().month)
        # search for unfinished records that are approved
        msgs = [i for i in results if i[13] == 1 and get_endtime(i) >= localtime()]
        msgs = sorted(msgs, key=get_endtime) # sort messages accoriding to their endtime
        num = len(msgs)
        return render_template('classroom_usage.html', msgs=msgs,
                               num=num)

@app.route('/personal_search/', methods=['GET', 'POST'])
def personal_search():
    if request.method == 'GET':
        return render_template('personal_search.html', hint = True)
    elif request.method == 'POST':
        with sqlite3.connect(DATABASE) as database:
            c = database.cursor()
            cursor = c.execute('select * from material where dep = ? and name = ?' ,(request.form['dep'], request.form['name']))
            mat_result = cursor.fetchall()
            cursor = c.execute('select * from classroom where dep = ? and name = ?' ,(request.form['dep'], request.form['name']))
            class_result = cursor.fetchall()
        num_mat = len(mat_result)
        num_class = len(class_result)
        return render_template('personal_search.html', hint = False, mat_result = mat_result, class_result=class_result, num_mat = num_mat, num_class = num_class)

#### views for administers ####

@app.route('/scrutiny-application/', methods=['GET', 'POST'])
@login_verify # to make sure non-administer can not access this page
def scrutiny():
    if request.method == 'GET':
        if 'id' in session:
            msgs = get_new_apply('MATERIAL', 0)
        elif 'id2' in session:
            msgs = get_new_apply('CLASSROOM', 0)
        id_list = [ i[0] for i in msgs ]
        num = len(id_list)
        return render_template('scrutiny.html', msgs=msgs,
                               num=num, id_list=id_list)
        # 此处id_list与 num都是为了解决提取出来的信息的定位问题。
        # id_list用于反馈时确定更新的申请id，而 msgs中的储存有数据内容
        # 的元组在该list中的位置则应由序数确定， 因而在scrutiny.html中
        # 将请求id号与序数做到了一一对应
        # 有更好方案可以改进


@app.route('/approve_mat/<int:id>', methods=['POST'])
@login_verify
def approve_mat(id):
    record_scrutiny_results('material', id, 1, session['id'])
    printLog("administer {} approved the application for borrowing material.\n application NO: {}\n".format(session['id'],id))
    flash("审批借出物资成功", category='success')
    return redirect(url_for('scrutiny'))

@app.route('/refuse_mat/<int:id>', methods=['POST'])
@login_verify
def refuse_mat(id):
    record_scrutiny_results('material', id, 2, session['id'])
    printLog("administer {} refused the application for borrowing material.\n application NO: {}\n".format(session['id'], id))
    flash("物资借出申请已拒绝", category='info')
    return redirect(url_for('scrutiny'))

@app.route('/approve_class/<int:id>', methods=['POST'])
@login_verify
def approve_class(id):
    record_scrutiny_results('classroom', id, 1, session['id2'])
    printLog("administer {} approved the application for borrowing classroom.\n application NO: {}\n".format(session['id2'],id))
    flash("审批借出教室成功", category='success')
    return redirect(url_for('scrutiny'))

@app.route('/refuse_class/<int:id>', methods=['POST'])
@login_verify
def refuse_class(id):
    record_scrutiny_results('classroom', id, 2, session['id2'])
    printLog("administer {} refused the application for borrowing classroom.\n application NO: {}\n".format(session['id2'], id))
    flash("教室借出申请已拒绝", category='info')
    return redirect(url_for('scrutiny'))

@app.route('/records/')
@login_verify
def records():
    if 'id' in session:
        tablename = 'material'
    elif 'id2' in session:
        tablename = 'classroom'
    results = get_records(tablename, expire_date().year, expire_date().month)
    num = len(results)
    return render_template('records.html', msgs = results, num = num)

######## Miscellaneous entries ########

@app.route('/opensource/')
def opensource_info():
    return render_template("opensource-info.html")

@app.route('/help/')
def help():
    return render_template("help.html")

######## run ########

if __name__ == '__main__':

    app.run(host = "127.0.0.1", debug = True)
