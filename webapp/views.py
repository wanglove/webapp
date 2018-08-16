from webapp import app
from flask import render_template, request, redirect, url_for, make_response, abort
from webapp.models import db, User


# 主页
@app.route('/')
def home_page():
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)
    return render_template('index.html', user=user)


# 视频汇总页面
@app.route('/videos')
def videos_page():
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)
    return render_template('videos.html', user=user)


# 视频详情
@app.route('/videos/<string:post_id>')
def show_video(post_id):
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)

    return render_template('post.html', user=user, post_id=post_id)


# 企业内推页面
@app.route('/jobs')
def jobs_page():
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)
    return render_template('jobs.html', user=user)


# 职位详情
@app.route('/jobs/<string:post_id>')
def show_job(post_id):
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)

    return render_template('post.html', user=user, post_id=post_id)


# 注册页面
@app.route('/register')
def reg_page():
    return render_template('register.html')


# 登陆页面
@app.route('/login')
def login_page():
    return render_template('login.html')


# 登出,删除cookie
@app.route('/logout')
def logout():

    # 设置http响应报文，删除cookie
    response = make_response(redirect(url_for('home_page')))
    response.set_cookie('token', 'deleted', max_age=0, path='/', httponly=True)

    return response


# 重置密码页面
@app.route('/resetpassword')
def reset_password_page():
    return render_template('resetpassword.html')


# 文章详情
@app.route('/posts/<string:post_id>')
def show_post(post_id):
    token = request.cookies.get('token')
    user = None
    if token:
        user = User.verify_auth_token(token)

    return render_template('post.html', user=user, post_id=post_id)


# 新建 文章页面
@app.route('/manage/posts/create')
def new_post():
    token = request.cookies.get('token')
    if token is None:
        abort(403)
    user = User.verify_auth_token(token)
    if user is None:
        abort(403)

    return render_template('manage_posts_edit.html', action='POST', user=user)


# 修改 文章页面
@app.route('/manage/posts/edit/<string:post_id>')
def edit_post(post_id):
    token = request.cookies.get('token')
    if token is None:
        abort(403)
    user = User.verify_auth_token(token)
    if user is None:
        abort(403)
    if post_id is None:
        abort(401)

    return render_template('manage_posts_edit.html', post_id=post_id, action='PUT', user=user)


# 管理文章页面
@app.route('/manage/posts')
def manage_posts():
    token = request.cookies.get('token')
    if token is None:
        abort(403)
    user = User.verify_auth_token(token)
    if user is None:
        abort(403)

    return render_template('manage_posts.html', user=user)
