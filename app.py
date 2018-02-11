#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from time import localtime, strftime
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
        cursor = c.execute('select * from %s where status = %d;'% (tablename, status_code))
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

        ##### 检查合法性 #####

#检查字符串中危险的特殊字符

def check_slashes(str):
    slashes=['{','}','\'','\"','%','?','\\',',',' ','-']
    for i in str:
        for t in slashes:
            if i==t:
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
def year_available(year):
    t=int(year)
    if t>=2018:
        return True
    else:
        flash("请输入正确的年份！", category="error")
        return False


def month_available(month):
    t=int(month)
    if t>=1 and t<=12:
        return True
    else:
        flash("请输入正确的月份！", category="error")
        return False


def day_available(day):
    t=int(day)
    if t>=1 and t<=31:
        return True
    else:
        flash("请输入正确的日期！", category="error")
        return False

def hour_available(hour):
    t=int(hour)
    if t>=0 and t<=23:
        return True
    else:
        flash("请输入正确的小时！",category="error")
        return False

def check_time(year, month, day, hour):
    if year_available(year) and month_available(month) and day_available(day) and hour_available(hour):
        return True
    else:
        return False

def legitimate(dic):
    items_1 = ('name', 'material', 'contact', 'dep')
    time_1 = ('startyear', 'startmonth', 'startday', 'starthour')
    time_2 = ('endingyear', 'endingmonth', 'endingday',  'endinghour')
    try:
        for item in items_1:
            if not check_slashes(dic[item]):
                return False
        if not name_available(dic['name']):
            return False
        if not email_available(dic['contact']):
            return False
        for time in [time_1, time_2]:
            if not check_time(dic[time[0]], dic[time[1]], dic[time[2]], dic[time[3]]):
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
                    pass
                flash("登陆成功！", category='success')
                return redirect(url_for('personal'))    # TODO: redirect error
            else:
                session.pop('id', None)
                session.pop('passwd', None)
                #session.pop('filename', None)
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
def approve_mat(id):
    record_scrutiny_results('material', id, 1, session['id'])
    printLog("administer {} approved the application for borrowing material.\n application NO: {}, approving time: {}\n ".format(session['id'],id, strftime("%Y-%m-%d %H:%M:%S", localtime())))
    flash("审批借出物资成功", category='success')
    return redirect(url_for('scrutiny'))


@app.route('/records/')
def records():
    return render_template('records.html')

######## Miscellaneous entries ########

@app.route('/opensource/')
def opensource_info():
    return render_template("opensource-info.html")

######## run ########

if __name__ == '__main__':

    app.run(host = "127.0.0.1", debug = True)
