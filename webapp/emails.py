from flask_mail import Mail
from flask_mail import Message

mail = Mail()


class MyMail():

    username = ''
    msg = '欢迎来到极客测试网站,您的验证码是:'

    def __init__(self, username, msg):
        self.username = username
        self.msg += msg

    def send_mail(self):
        msg = Message(self.msg, recipients=[self.username])
        mail.send(msg)
