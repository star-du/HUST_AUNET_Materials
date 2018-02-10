#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
from time import gmtime, strftime
import sqlite3, os


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
        applying_material(request.form)
        printLog("user {} apply for material: {}, submitting time: {}".format(request.form['name'], request.form['material'], strftime("%Y-%m-%d %H:%M:%S", gmtime())))
        flash("表格提交成功", category='success')
        return redirect(url_for('personal'))


######## Miscellaneous entries ########

@app.route('/opensource/')
def opensource_info():
    return render_template("opensource-info.html")

######## run ########

if __name__ == '__main__':

    app.run(host = "127.0.0.1", debug = True)
