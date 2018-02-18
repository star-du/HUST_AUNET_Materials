#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.header import Header

sender = '1457372615@qq.com' #发件人邮箱账号
passWord = 'fjobxupauuwfighf'   #发件人邮箱授权码
receivers = ['1516274933@qq.com']   #发件人的邮箱账号
'''
此处有个问题:receivers必须主动开启smtp/pop服务，所以可能需要在主页上进行说明
附上qq开启smtp/pop服务的链接：https://jingyan.baidu.com/article/fedf0737af2b4035ac8977ea.html
'''

def mail():
    ret = True
    try:
        msg = MIMEMultipart()
        msg['From'] = Header('华中大社团联合会', 'utf-8')
        msg['To'] = Header('社联的小伙伴', 'utf-8')
        subject = '来自社联的温馨提醒'
        msg['Subject'] = Header(subject, 'utf-8')
        msg = MIMEText('您已成功提交申请，请勿重复提交!', 'plain', 'utf-8')
        s = smtplib.SMTP_SSL("smtp.qq.com",465) #第三方服务器及其端口
        s.set_debuglevel(1)
        s.login(sender,passWord)
        #给列表中所有receiver发送邮件
        for i in range(len(receivers)):
            to = receivers[i]
            msg['To'] = to
            s.sendmail(sender,to,msg.as_string())
            print('success')
        s.quit()
    except smtplib.SMTPException as e:
        ret = False
    return ret
ret = mail()
if ret:
    print("success")
else:
    print("fail")
