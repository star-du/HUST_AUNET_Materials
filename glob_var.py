""" global configuration """
import os

SYSTEM_ROOT = os.path.split(os.path.realpath(__file__))[0]
DATABASE = os.path.join(SYSTEM_ROOT, 'data.db')

# for email_module
# NOTE: NEED A VALID EMAIL_SENDER ADDRESS AND PASSCODE ('授权码')
email_sender = '1043361205@qq.com'
email_pass = None
