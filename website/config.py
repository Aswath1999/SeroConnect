import os
from decouple import config

# main config
SECRET_KEY = 'nakflanfak'
SECURITY_PASSWORD_SALT = 'mjknacjknfkjn'
DEBUG = False
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = config('GMAIL')
MAIL_PASSWORD = config('PASSWORD')

# mail accounts
MAIL_DEFAULT_SENDER = 'from@example.com'