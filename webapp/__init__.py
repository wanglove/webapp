from flask import Flask
from flask_restful import Api
from webapp.models import db, bcrypt
from webapp.resources.users import UsersApi
from webapp.resources.auth import AuthApi
from webapp.resources.captchas import CaptchaApi
from webapp.resources.posts import PostApi
from webapp.resources.categories import CategoryApi
from webapp.resources.carousels import CarouselApi
from webapp.resources.syssettings import SyssetingsApi
from webapp.emails import mail


# flask应用实例
app = Flask(__name__)
# 读取配置文件
app.config.from_object('webapp.config')

# 初始化数据库应用
db.init_app(app)

# 如果没有表,创建表
db.create_all(app=app)

# 初始化邮件发送实例
mail.init_app(app)

# 初始化hash算法实例
bcrypt.init_app(app)

# 挂载和初始化restful api
restful_api = Api()
restful_api.add_resource(UsersApi, '/api/users')
restful_api.add_resource(AuthApi, '/api/authenticate')
restful_api.add_resource(CaptchaApi, '/api/captchas')
restful_api.add_resource(PostApi, '/api/posts', '/api/posts/<string:post_id>')
restful_api.add_resource(CategoryApi, '/api/posts/categories')
restful_api.add_resource(CarouselApi, '/api/carousels')
restful_api.add_resource(SyssetingsApi, '/api/syssettings')
restful_api.init_app(app)

import webapp.views
