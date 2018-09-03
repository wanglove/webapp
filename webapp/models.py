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


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='文章id')
    userid = db.Column(db.String(50), comment='作者用户id')
    nickname = db.Column(db.String(50), comment='作者昵称')
    post_type = db.Column(db.String(50), default='文章', comment='文章类型,文章,视频,企业内推')
    title = db.Column(db.String(50), comment='文章标题')
    image = db.Column(db.String(256), comment='封面图片')
    category = db.Column(db.String(50), nullable=False, comment='文章分类')
    tags = db.Column(db.String(256), comment='文章标签')
    summary = db.Column(db.String(200), comment='文章摘要')
    content = db.Column(db.Text, comment='文章内容')
    page_view = db.Column(db.Integer, default=0, comment='文章浏览数')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp(), comment='更新时间')

    def __init__(self, userid, nickname, post_type, title, image, category, tags, summary, content):
        self.userid = userid
        self.nickname = nickname
        self.post_type = post_type
        self.title = title
        self.image = image
        self.category = category
        self.tags = tags
        self.summary = summary
        self.content = content


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='分类id')
    category = db.Column(db.String(50), nullable=False, unique=True, comment='分类名称')
    type = db.Column(db.String(5), default='00000', comment='分类类型')

    def __init__(self, category, type):
        self.category = category
        self.type = type


class Carousel(db.Model):
    __tablename__ = 'carousels'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    postid = db.Column(db.Integer, comment='文章id')
    position = db.Column(db.String(1), default='1', comment='轮播图片展示位置,1=首页')
    title = db.Column(db.String(50), comment='文章标题')
    image = db.Column(db.String(256), comment='封面图片')
    summary = db.Column(db.String(200), comment='文章摘要')


class Syssetting(db.Model):
    __tablename__ = 'syssetings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    index_notice = db.Column(db.Text, comment='首页的公告内容')
    video_notice = db.Column(db.Text, comment='视频页的公告内容')
    job_notice = db.Column(db.Text, comment='企业内推页的公告内容')


class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='评论id')
    postid = db.Column(db.Integer, comment='文章id')
    userid = db.Column(db.String(50), comment='作者用户id')
    nickname = db.Column(db.String(50), comment='作者昵称')
    content = db.Column(db.Text, comment='评论内容')
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp(), comment='更新时间')
