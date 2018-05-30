from flask_restful import Resource, reqparse
from webapp.models import Captcha, db
from webapp.emails import MyMail
from time import time, mktime, strptime


class CaptchaApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form', required=True, help='邮箱地址不能为空')

    # 用户获取验证码
    def post(self):
        # 解析POST请求上送的参数
        args = self.parser.parse_args()

        captcha = Captcha.query.filter_by(username=args.username).first()
        if captcha is None:
            new_captcha = Captcha(args.username)
            db.session.add(new_captcha)
            db.session.commit()
            # 发邮件验证码
            email = MyMail(args.username, new_captcha.captcha)
            email.send_mail()
            return {'message': '验证码已经发送邮箱,10分钟内有效,请勿重复点击获取'}, 201
        else:
            now_time_seconds = time()
            create_time_seconds = mktime(strptime(str(captcha.create_time), "%Y-%m-%d %H:%M:%S"))

            # 验证码创建时间大于10分钟，重新生成
            if now_time_seconds - create_time_seconds >= 10*60:
                db.session.delete(captcha)
                db.session.commit()
                # 删除过期验证码之后，创建新的验证码
                new_captcha = Captcha(args.username)
                db.session.add(new_captcha)
                db.session.commit()
                # 发邮件验证码
                email = MyMail(args.username, new_captcha.captcha)
                email.send_mail()

            return {'message': '验证码已经发送邮箱,10分钟内有效,请勿重复点击获取'}, 200






