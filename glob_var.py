""" global configuration """
import os

SYSTEM_ROOT = os.path.split(os.path.realpath(__file__))[0]
DATABASE = os.path.join(SYSTEM_ROOT, 'data.db')
LOG = os.path.join(SYSTEM_ROOT, 'log.txt')
SALT = 'HUSTAUNET' # used as salt for hash function

# for email_module
# if email_enable = True and email_sender, email_pass are correctly
#given, notice will be sent via email.
email_enable = False
# NOTE: NEED A VALID EMAIL_SENDER ADDRESS AND PASSCODE ('授权码')
email_sender = None
email_pass = None
