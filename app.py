#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from time import localtime, strftime, strptime
from datetime import date, timedelta
from functools import wraps
import sqlite3, os ,re#正则


######## global configuration ########
SYSTEM_ROOT = os.path.split(os.path.realpath(__file__))[0]
DATABASE = os.path.join(SYSTEM_ROOT, 'data.db')
######## initializaton ########

app = Flask(__name__)
app.secret_key = 's\x1f}\xc8\xe29c\x84\xd1\x87P\x8e\xa5h5s\xf1\xfff\xcf\xfcK\xe8i'

######## user utils ########
def verify(id,passwd):
    with sqlite3.connect(DATABASE) as database:
        cursor = database.execute("SELECT PASSWORD FROM ADMIN WHERE ID = ? ", (id,))
        correct = cursor.fetchone()
        if correct == None:  # wrong id
            flash("用户名不存在！", category="error")
            return False
        else:  # correct id
            if passwd == correct[0]:
                return True    # correct id-pass pair
            else:  # wrong passwd
                flash("密码错误！", category="error")
                return False

def printLog(log):
    ''' Use to write log for user's behaviour '''
    with open("log.txt",encoding="utf-8", mode='a') as f:
        f.write(log+"\n")

def applying_material(form):
    ''' Use to dump the applying information into the database, using the request.form as argument '''
    mat_form = [(form['dep'], form['name'], form['material'], form['contact'], form['startyear'], form['startmonth'], form['startday'], form['starthour'], form['endingyear'], form['endingmonth'], form['endingday'], form['endinghour'])]
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        c.executemany('INSERT INTO MATERIAL VALUES (NULL,?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, 0, NULL)', mat_form)
        # I note that the first null value is _needed_ for the index (the integer-based prime key) to AUTOINCREMENT, and it seems to be the so called 'ROWID' column
        # maybe should check : https://stackoverflow.com/questions/7905859/is-there-an-auto-increment-in-sqlite
        database.commit()

def get_new_apply(tablename, status_code):
    ''' Take the name of the table and status_code that is  checked as the arguments, return the list of complete content of matching records. Items in the list are tuples.

    Tablename should be a string and status_code is expected to be integers 0, 1, 2.
    '''
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        cursor = c.execute('select * from %s where status = %d;'% (tablename, status_code)) # 这里不是binding，好像不能用？占位
        new_apply_list = cursor.fetchall() # fetchall() returns a list of  tuples
        return new_apply_list


def record_scrutiny_results(tablename, indx, status_code, admin):
    ''' Take the name of the table, index of application and the renewed status_code, name of admin as arguments, the function updates the status of application on demand.

    Note that under normal condition, status_code should be 1 (representing approval of application) or 2 (representing denial)'''
    with sqlite3.connect(DATABASE) as database:
        c = database.cursor()
        c.execute("update %s set STATUS = ? where ID = ? "%tablename , (status_code, indx)  )
        c.execute("update %s set ADMIN = ? where ID = ? "%tablename , (admin, indx)  )
        database.commit()

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
        if 'id' not in session:
            flash("请登录！", category="error")     # NOTE: flash-msg show in the NEXT page
            return redirect(url_for('login'))
        return to_be_decorated(*args, **kwargs)
    return decorated

        ##### 检查合法性 #####

#检查字符串中危险的特殊字符

def check_slashes(str):
    slashes=['{','}','\'','\"','%','?','\\',',']
    for i in str:
            if i in slashes:
                flash("输入中包含非法字符", category="error")
                return False

    return True


#检查邮箱格式
def email_available(email):#email :str 格式
    pattern = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
    match = pattern.match(email)
    if match:
        return True
    else:
        flash("邮箱格式不正确！", category="error")
        return False


#检查姓名格式
def name_available(name):#name :str 格式
    pattern = re.compile(r"[\u4e00-\u9fa5]{2,4}")#匹配2到4个汉字
    match = pattern.match(name)
    if match:
        return True
    else:
        flash("不是合法的姓名！", category="error")
        return False


#检查日期格式
#original version
# def year_available(year):
#     if not isinstance(year, int):
#         flash("请输入正确的年份！", category="error")
#         return False
#     if not year >= 2000:
#         flash("请输入正确的年份！", category="error")
#         return False
#     else:
#         return True
#
#
# def month_available(month):
#     if not isinstance(month, int):
#         flash("请输入正确的月份！", category="error")
#         return False
#     if not month in range(1,13):
#         flash("请输入正确的月份！", category="error")
#         return False
#     else:
#         return True
#
# def day_available(day):
#     if not isinstance(month, int):
#         flash("请输入正确的月份！", category="error")
#         return False
#     if not day in range(1, 31):
#         flash("请输入正确的月份！", category="error")
#         return False
#     else:
#         return True
#
# def hour_available(hour):
#     t=int(hour)
#     if t>=0 and t<=23:
#         return True
#     else:
#         flash("请输入正确的小时！",category="error")
#         return False

def struct(year, month, day, hour):
    ''' Take **strings** as arguments, return a struct_time instance if it represents time with given format, else return _None_ '''
    try:
        struct_time1 = strptime(year + ' ' + month + ' ' + day + ' ' + hour, '%Y %m %d %H')
        return struct_time1
    except:
        flash("请输入正确的时间信息！",category="error")
        return None

def legitimate(dic):
    items_1 = ('name', 'material', 'contact', 'dep')
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
        t1 = struct(*start)
        t2 = struct(*end)
        if t1 == None or t2 == None:
            return False
        elif t2 <= t1 or t1 <= localtime():
            flash("请输入正确的时间信息！",category="error")
            return False
        return True
    except :
        flash('INVALID REQUEST', category='error')
        return False


######## views  ########
    ''' entry & exit '''
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if check_slashes(request.form['id']) and check_slashes(request.form['passwd']):#检查危险字符
            session['id'] = request.form['id']
            session['passwd'] = request.form['passwd']
            if verify(session['id'], session['passwd']):
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
        else:
            return redirect(url_for('login'))

@app.route('/home/')
def personal():
    return render_template("home.html")

@app.route('/logout/')
def logout():
    # 已登陆的管理员才能看到logout按钮，否则报错
    assert 'id' in session
        # clear session
    session.pop('id', None) # about the usage of session.pop see: https://stackoverflow.com/questions/20115662/what-does-the-second-argument-of-the-session-pop-method-do-in-python-flask
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
        # TODO MAKE IT LOOK GOOD!
        if legitimate(request.form):
            applying_material(request.form)
            printLog("user {} apply for material: {}, submitting time: {}\n".format(request.form['name'], request.form['material'], strftime("%Y-%m-%d %H:%M:%S", localtime())))
            flash("表格提交成功", category='success')
            return redirect(url_for('personal'))
        else:
            return render_template('materials_apply.html')


@app.route('/scrutiny-application/', methods=['GET', 'POST'])
@login_verify # to make sure non-administer can not access this page
def scrutiny():
    if request.method == 'GET':
        msgs = get_new_apply('MATERIAL', 0)
        id_list = [ i[0] for i in msgs ]
        num = len(id_list)
        return render_template('scrutiny.html', msgs = msgs, num = num, id_list = id_list)
        # 此处id_list与 num都是为了解决提取出来的信息的定位问题。
        # id_list用于反馈时确定更新的申请id，而 msgs中的储存有数据内容
        # 的元组在该list中的位置则应由序数确定， 因而在scrutiny.html中
        # 将请求id号与序数做到了一一对应
        # 有更好方案可以改进


@app.route('/approve_mat/<int:id>', methods=['POST'])
@login_verify
def approve_mat(id):
    record_scrutiny_results('material', id, 1, session['id'])
    printLog("administer {} approved the application for borrowing material.\n application NO: {}, approving time: {}\n".format(session['id'],id, strftime("%Y-%m-%d %H:%M:%S", localtime())))
    flash("审批借出物资成功", category='success')
    return redirect(url_for('scrutiny'))

@app.route('/refuse_mat/<int:id>', methods=['POST'])
@login_verify
def refuse_mat(id):
    record_scrutiny_results('material', id, 2, session['id'])
    printLog("administer {} refused the application for borrowing material.\n application NO: {}, approving time: {}\n ".format(session['id'],id, strftime("%Y-%m-%d %H:%M:%S", localtime())))
    flash("物资借出申请已拒绝", category='info')
    return redirect(url_for('scrutiny'))

@app.route('/records/')
@login_verify
def records():
    results = get_records('material',expire_date().year, expire_date().month)
    num = len(results)
    return render_template('records.html', msgs = results, num = num)

######## Miscellaneous entries ########

@app.route('/opensource/')
def opensource_info():
    return render_template("opensource-info.html")

######## run ########

if __name__ == '__main__':

    app.run(host = "127.0.0.1", debug = True)
