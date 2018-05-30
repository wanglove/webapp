from webapp import app
from flask import render_template


# 主页
@app.route('/')
def home_page():
    return render_template('index.html')


# 注册页面
@app.route('/register')
def reg_page():
    return render_template('register.html')


# 登陆页面
@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/resetpassword')
def reset_password_page():
    return render_template('resetpassword.html')

