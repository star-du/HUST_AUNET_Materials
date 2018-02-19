import smtplib
from glob_var import *
from email.mime.text import MIMEText
from email.header import Header
# from email.utils import formataddr
# from email.mime.multipart import MIMEMultipart

'''
此处有个问题:receivers必须主动开启smtp/pop服务，所以可能需要在主页上进行说明
附上qq开启smtp/pop服务的链接：https://jingyan.baidu.com/article/fedf0737af2b4035ac8977ea.html
'''


def mail(content,receivers):
    """ Send email with given content to receivers.

    First argument is expected to be a string and the second one should be a **list or tuple** (use syntax like '(item,)' if there is only one receiver). Return True if no errors occurs. """
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header('华中大社团联合会', 'utf-8')
        msg['To'] = Header('社联的小伙伴', 'utf-8')
        subject = '来自社联的温馨提醒'
        msg['Subject'] = Header(subject, 'utf-8')
        s = smtplib.SMTP_SSL("smtp.qq.com",465) #第三方服务器及其端口
        # s.set_debuglevel(1)
        s.login(email_sender, email_pass)
        #给列表中所有receiver发送邮件
        for i in range(len(receivers)):
            to = receivers[i]
            msg['To'] = to
            s.sendmail(email_sender,to,msg.as_string())
            print("success")
        s.quit()
    except smtplib.SMTPException:
        print("邮件发送失败")
        return False
    print("邮件发送成功")
    return True
