from flask_restful import Resource, reqparse
from webapp.models import User, Captcha, db


class UsersApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nickname', type=str, location='form')
        self.parser.add_argument('username', type=str, location='form', required=True, help='用户名不能为空')
        self.parser.add_argument('captcha', type=str, location='form', required=True, help='验证码不能为空')
        self.parser.add_argument('password', type=str, location='form', required=True, help='密码不能为空')
        self.parser.add_argument('phone', type=str, location='form')

    # 用户注册接口
    def post(self):
        # 解析POST请求上送的参数
        args = self.parser.parse_args()

        user = User.query.filter_by(username=args.username).first()
        if user:
            return {'message': '邮箱地址已经被注册'}, 400

        # 校验验证码
        captcha = Captcha.query.filter_by(username=args.username).first()
        if captcha is None:
            return {'message': '请填写注册邮箱中收到的验证码'}, 400

        is_too_many_try = captcha.verify_captcha_too_many_try()
        if is_too_many_try:
            return {'message': '短时间内输入验证码失败超过3次，请10分钟后重新获取新验证码'}, 400

        if not captcha.verify_captcha_code(args.captcha):
            return {'message': '验证码输入有误'}, 400

        # 新建用户
        new_user = User(username=args.username, password=args.password,\
                       nickname=args.nickname, phone=args.phone)

        try:
            db.session.add(new_user)
            db.session.delete(captcha)   # 注册过后，验证码删除
            db.session.commit()
            return {'message': '注册成功'}, 201
        except:
            db.session.rollback()
            return {'message': '输入有误'}, 400


    # 重置密码功能
    def put(self):
        # 解析POST请求上送的参数
        args = self.parser.parse_args()

        user = User.query.filter_by(username=args.username).first()
        if user is None:
            return {'message': '邮箱地址不存在'}, 400

        # 校验验证码
        captcha = Captcha.query.filter_by(username=args.username).first()

        if captcha is None:
            return {'message': '请填写注册邮箱中收到的验证码'}, 400

        is_too_many_try = captcha.verify_captcha_too_many_try()
        if is_too_many_try:
            return {'message': '短时间内输入验证码失败超过3次，请10分钟后重新获取新验证码'}, 400

        if not captcha.verify_captcha_code(args.captcha):
            return {'message': '验证码输入有误'}, 400

        # 重置密码
        user.set_password(args.password)
        db.session.delete(captcha)  # 验证码删除
        db.session.commit()
        return {'message': '密码重置成功'}, 201








