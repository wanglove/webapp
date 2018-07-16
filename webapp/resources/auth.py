from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_restful import Resource, reqparse
from webapp.models import User


# 用户授权api
class AuthApi(Resource):

    # 用户登陆接口
    def post(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form', required=True, help='用户名不能为空')
        self.parser.add_argument('password', type=str, location='form', required=True, help='密码不能为空')

        args = self.parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        # 根据用户名找不到用户，直接返回401
        if user is None:
            return {'message': '用户名或密码错误'}, 401

        # 用户存在，密码正确
        if user.check_password(args['password']):
            serializer = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=current_app.config['TOKEN_EXPIRES_TIME'])
            new_token = serializer.dumps({'id': user.id}).decode()

            return {'message': '登陆成功'}, 200, {'Set-Cookie': 'token=%s;Domain=0.0.0.0;Path=/;HttpOnly'%new_token}
        # 用户存在，密码输错
        else:
            return {'message': '用户名或密码错误'}, 401

    # 用户登出
    def delete(self):

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str, location='cookies', required=True, help='用户无授权')

        args = self.parser.parse_args()

        if args.token is None:
            return {'message': '用户无授权'}, 401

        user = User.verify_auth_token(args.token)
        if user is None:
            return {'message': '用户授权无效或过期'}, 401, \
                   {'Set-Cookie': 'token=deleted;Domain=0.0.0.0;Path=/;Max-age=0;HttpOnly'}

        return {'message': '用户登出成功'}, 204,\
               {'Set-Cookie': 'token=deleted;Domain=0.0.0.0;Path=/;Max-age=0;HttpOnly'}
