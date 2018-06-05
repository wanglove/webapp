from webapp import app
from flask import render_template, request, redirect, url_for, make_response
from webapp.models import db, User, UserLoginContrl


# 主页
@app.route('/')
def home_page():
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)
    return render_template('index.html', user=user)


# 注册页面
@app.route('/register')
def reg_page():
    return render_template('register.html')


# 登陆页面
@app.route('/login')
def login_page():
    return render_template('login.html')


# 登出
@app.route('/logout')
def logout():

    # 设置http响应报文，删除cookie
    response = make_response(redirect(url_for('home_page')))
    response.set_cookie('token', 'deleted', max_age=0, path='/', domain='0.0.0.0', httponly=True)

    # 从请求中拿出cookie
    token = request.cookies.get('token')

    if token is None:
        return response

    user = User.verify_auth_token(token)
    if user is None:
        return response

    # 登出的token要与控制表里的一致,删除该用户登陆控制表中的数据
    user_ctl = UserLoginContrl.query.get(user.id)
    if user_ctl and user_ctl.token == token:
        db.session.delete(user_ctl)
        db.session.commit()
        return response
    else:
        return response


@app.route('/resetpassword')
def reset_password_page():
    return render_template('resetpassword.html')

