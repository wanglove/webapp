import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# token有效期,单位秒
TOKEN_EXPIRES_TIME = 6000

# 数据库链接配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/geektest?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮件模块配置
MAIL_SERVER = 'smtp.126.com'
MAIL_PORT = 25
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

# 文章分页,每页显示多少条目数
POSTS_PER_PAGE = 20
