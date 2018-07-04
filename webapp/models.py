from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from uuid import uuid4
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import current_app
import random

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True, comment='用户id')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名(邮箱)')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    nickname = db.Column(db.String(255), nullable=False, comment='昵称')
    phone = db.Column(db.String(13), comment='手机号码')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='账号创建时间')
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp(), comment='账号变更时间')
    is_active = db.Column(db.String(1), default='1', comment='账户状态:激活=1|锁定=0')

    def __init__(self, username, password, nickname, phone):
        self.id = str(uuid4())
        self.username = username
        self.set_password(password)
        self.nickname = nickname
        self.phone = phone

    # 加密
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        return self.password

    # 检查用户上传的密码
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    # 校验token是否正确有效
    def verify_auth_token(token):
        serializer = Serializer(
            current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.filter_by(id=data['id']).first()
        return user


class Captcha(db.Model):
    __tablename__ = 'captcha'

    username = db.Column(db.String(50), nullable=False, primary_key=True, comment='用户名(邮箱)')
    captcha = db.Column(db.String(10), nullable=False, comment='验证码')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    try_num = db.Column(db.Integer, default=0, comment='尝试输入验证码的次数')

    def __init__(self, username):
        self.username = username
        self.captcha = str(random.randint(100000, 999999))

    # 校验验证码
    def verify_captcha_code(self, captcha):
        if self.captcha != captcha:
            return False
        else:
            return True

    # 3次输入不正确，锁定10min钟，防止暴力破解
    def verify_captcha_too_many_try(self):
        self.try_num += 1
        db.session.commit()

        if self.try_num > 3:
            return True
        else:
            return False

class UserLoginContrl(db.Model):

    __tablename__ = 'user_login_contrl'
    id = db.Column(db.String(45), primary_key=True, comment='用户id')
    username = db.Column(db.String(50), nullable=False, unique=True, comment='用户名(邮箱)')
    token = db.Column(db.String(255), comment='用户token')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='登陆时间')

    def __init__(self, id, username, token=None):
        self.id = id
        self.username = username
        self.token = token

    def verify_user_single_login(uid, token):
        user_ctl = UserLoginContrl.query.get(uid)
        if user_ctl:
            if user_ctl.token == token:
                return True
        else:
            return False


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True, comment='文章id')
    userid = db.Column(db.String(50), comment='作者用户id')
    username = db.Column(db.String(50), comment='作者用户名')
    title = db.Column(db.String(50), comment='文章标题')
    summary = db.Column(db.String(200), comment='文章摘要')
    content = db.Column(db.Text, comment='文章内容')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp(), comment='更新时间')

    def __init__(self, userid, username, title, summary, content):
        self.id = str(uuid4())
        self.userid = userid
        self.username = username
        self.title = title
        self.summary = summary
        self.content = content


class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.String(45), primary_key=True, comment='评论id')
    blogid = db.Column(db.String(45), comment='文章id')
    userid = db.Column(db.String(50), comment='作者用户id')
    username = db.Column(db.String(50), comment='作者用户名')
    content = db.Column(db.Text, comment='评论内容')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp(), comment='更新时间')
