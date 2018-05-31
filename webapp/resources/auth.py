from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_restful import Resource, reqparse
from webapp.models import User


# 用户授权api
class AuthApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form', required=True, help='用户名不能为空')
        self.parser.add_argument('password', type=str, location='form', required=True, help='密码不能为空')

    def post(self):

        args = self.parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user is None:
            return {'message': '用户名或密码错误'}, 401

        # 判断密码是否和用户表中的一致
        if user.check_password(args['password']):
            # serializer object will be saved the token period of time.
            serializer = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600)
            new_token = serializer.dumps({'id': user.id}).decode()
            return {'token': new_token}, 200, {'Set-Cookie': 'token=%s;Domain=0.0.0.0;Path=/;HttpOnly'%new_token}
        else:
            return {'message': '用户名或密码错误'}, 401
