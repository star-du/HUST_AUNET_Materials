#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
from flask import make_response, flash, jsonify, send_from_directory
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
        cursor = database.execute("select password from admin where id = ? ", (id,))
        correct = cursor.fetchone()
        if correct==None:  # wrong id
            flash("用户名或密码错误！", category="error")
            return False
        else:  # correct id
            if passwd ==correct[0]:
                return True    # correct id-pass pair
            else:  # wrong passwd
                flash("用户名或密码错误！", category="error")
                return False

######## views ########
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
            return redirect(url_for('personal'))
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
    session.pop('id', None)
    print(session.pop('passwd', None))  # should get `None`
    session.pop('filename', None)
    flash("已登出", category='message')
    return redirect(url_for('index'))
######## Miscellaneous entries ########

@app.route('/opensource/')
def opensource_info():
    return render_template("opensource-info.html") # 此html可以直接沿用吧？


######## run ########

if __name__ == '__main__':

    app.run(host="127.0.0.1", debug=True)
