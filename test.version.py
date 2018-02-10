#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
发送text文本邮件(测试版）
测试前确保自己邮箱的smpt协议开启。否则会有点尴尬
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#第三方 SMTP 服务
'''
这一块测试时可以不用
'''
mail_host = "smtp.XXX.com" #设置服务器
mail_user = "XXXX" # 用户名
mail_pass = "XXXXXX" #口令

sender = 'AAA@AA.com'
receivers = ['WWW@WW.com']  # 接收邮件

#第一个参数为文本内容，plain设置文本格式，utf_8设置编码格式
message = MIMEText('~~~~','plain','utf-8')
message['From'] = Header("测试",'utf-8')
message['To'] = Header('测试','utf-8')

subject =  'Python SMTP 邮件测试'
message['Subject'] = Header(subject,'utf-8')

try:
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender,receivers,message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error:无法发送邮件")
