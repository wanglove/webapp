from flask import current_app
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from webapp.models import db, User, Post


post_data = {
    'id': fields.String,
    'userid': fields.String,
    'username': fields.String,
    'title': fields.String,
    'summary': fields.String,
    'content': fields.String,
    'create_time': fields.DateTime(dt_format='iso8601'),
    'update_time': fields.DateTime(dt_format='iso8601')
}

posts_fields = {
    'page': fields.Integer(default=0),
    'pages': fields.Integer(default=0),
    'has_prev': fields.Boolean(default=False),
    'has_next': fields.Boolean(default=False),
    'posts': fields.List(fields.Nested(post_data))   # list返回多条数据
}


class PostApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page', type=int)
        self.parser.add_argument('per_page', type=int)
        self.parser.add_argument('title', type=str)
        self.parser.add_argument('summary', type=str)
        self.parser.add_argument('content', type=str)
        self.parser.add_argument('token', type=str, location='cookies')

    @marshal_with(posts_fields)
    def get(self, post_id=None):
        # 根据pst_id查询
        if post_id:
            post = Post.query.get(post_id)
            if post:
                return {'posts': post}, 200
            else:
                abort(404)
        # 分页查询
        else:

            args = self.parser.parse_args()

            # 设置查询的分页,默认分页是1
            page = 1
            if args.page is not None and args.page > 0:
                page = args.page
            # 设置每页显示多少条数据
            if args.per_page is not None and args.per_page > 0:
                per_page = args.per_page
            else:
                per_page = current_app.config['POSTS_PER_PAGE']

            pagination = Post.query.order_by(Post.update_time.desc()).\
                paginate(page, per_page=per_page, error_out=False)

            posts = pagination.items     # 分页内容
            page = pagination.page       # 当前分页数
            pages = pagination.pages     # 总分页数
            has_prev = pagination.has_prev   # 是否有上一页
            has_next = pagination.has_next   # 是否有下一页

            return {'page': page, 'pages': pages, 'has_prev': has_prev,
                    'has_next': has_next, 'posts': posts}, 200

    # 新增文章
    def post(self):

        args = self.parser.parse_args()
        # 校验参数必须填写
        if args.title is None or args.summary is None or args.content is None:
            abort(401)

        # 校验用户身份 admin用户允许新增文章
        if args.token is None:
            abort(403)
        user = User.verify_auth_token(args.token)
        if user is None:
            abort(403)
        if user.username != '251319710@qq.com':
            abort(403)

        new_post = Post(user.id, user.username, args.title, args.summary, args.content)
        db.session.add(new_post)
        db.session.commit()

    # 修改文章
    def put(self, post_id):

        args = self.parser.parse_args()
        # 校验参数必须填写
        if args.title is None or args.summary is None or args.content is None:
            abort(401)

        # 校验用户身份 admin用户允许新增文章
        if args.token is None:
            abort(403)
        user = User.verify_auth_token(args.token)
        if user is None:
            abort(403)
        if user.username != '251319710@qq.com':
            abort(403)

        # 根据文章id找出文章，然后修改
        post = Post.query.get(post_id)
        if post:
            post.title = args.title
            post.summary = args.summary
            post.content = args.content
            db.session.commit()
            return {'message': '更新成功'}, 201
        else:
            abort(404)

    # 根据id删除文章
    def delete(self, post_id):
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return {'message': '删除成功'}, 201
        else:
            abort(404)
