import os

SECRET_KEY = os.urandom(24)

# 数据库链接配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/geektest?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

# 邮件模块配置
MAIL_SERVER = 'smtp.126.com'
MAIL_PORT = 25
MAIL_USERNAME = 'wanglove@126.com'
MAIL_PASSWORD = '********'
MAIL_DEFAULT_SENDER = 'wanglove@126.com'
