#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''   Material System build   '''

######## importing ########
from flask import Flask, request, session, render_template, url_for, redirect
import sqlite3

######## global configuration ########

######## initializaton ########

app = Flask(__name__)
app.secret_key = 's\x1f}\xc8\xe29c\x84\xd1\x87P\x8e\xa5h5s\xf1\xfff\xcf\xfcK\xe8i'

######## user utils ########
def verify(id,passwd):
    pass

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

@app.route('/registering/', methods=['POST'])
def register():
    id = request.form.get('id', '')
    passwd = request.form.get('passwd_first', '')
    if passwd != request.form.get('passwd_second', ''):
        # TODO: if using 'warning', will toast an empty warning and then the info-toast containning the message
        flash("两次密码不相同！<br>换个好记一点的吧？", category='warning')
        return redirect(url_for('login'))
    elif len(passwd) < 8:
        flash("密码太短了！", category='warning')
        return redirect(url_for('login'))
    elif request.form.get('invitation', '') != INVITATION:
        flash("邀请码错误！", category='warning')
        return redirect(url_for('login'))
    else:
        if adminRegist(id, passwd):
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    if 'id' in session:
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
