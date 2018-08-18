from flask import current_app
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from webapp.models import db, User, Post


post_data = {
    'id': fields.Integer,
    'userid': fields.String,
    'nickname': fields.String,
    'post_type': fields.String,
    'title': fields.String,
    'image': fields.String,
    'category': fields.String,
    'tags': fields.String,
    'summary': fields.String,
    'content': fields.String,
    'page_view': fields.Integer,
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
        self.parser.add_argument('post_type', type=str)
        self.parser.add_argument('title', type=str)
        self.parser.add_argument('image', type=str)
        self.parser.add_argument('category', type=str)
        self.parser.add_argument('summary', type=str)
        self.parser.add_argument('tags', type=str)
        self.parser.add_argument('content', type=str)
        self.parser.add_argument('page_view', type=str)
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
        # 按分类分页查询
        else:

            args = self.parser.parse_args()

            # 按浏览次数多少,默认倒序
            page_view = ''
            if args.page_view is not None:
                page_view = args.page_view

            # 设置要查询的文章类型
            post_type = ''
            if args.post_type is not None:
                post_type = args.post_type

            # 设置查询分类
            category = ''
            if args.category is not None:
                category = args.category

            # 设置查询的分页,默认分页是1
            page = 1
            if args.page is not None:
                if args.page > 0:
                    page = args.page

            # 设置每页显示多少条数据,每页面最多显示20条数据
            per_page = current_app.config['POSTS_PER_PAGE']
            if args.per_page is not None:
                if args.per_page > 0 and args.per_page <= 20:
                    per_page = args.per_page

            # 查询所有的文章,按时间倒序查询
            if category == '' and post_type == '' and page_view == '':
                pagination = Post.query.order_by(Post.create_time.desc()). \
                    paginate(page, per_page=per_page, error_out=False)
            # 按浏览次数倒查询所有文章,7日热门和30日热门
            elif category == '' and post_type == '' and page_view == 'desc':
                pagination = Post.query.order_by(Post.page_view.desc()). \
                    paginate(page, per_page=per_page, error_out=False)
            # 按分类倒序查询
            elif category != '' and post_type == '':
                pagination = Post.query.filter_by(category=category).order_by(Post.create_time.desc()). \
                    paginate(page, per_page=per_page, error_out=False)
            # 按文章类型倒序查询
            elif category == '' and post_type != '':
                pagination = Post.query.filter_by(post_type=post_type).order_by(Post.create_time.desc()). \
                    paginate(page, per_page=per_page, error_out=False)
            # 按类型和分类查询,倒序输出
            elif category != '' and post_type != '':
                pagination = Post.query.filter_by(category=category, post_type=post_type)\
                    .order_by(Post.create_time.desc()).paginate(page, per_page=per_page, error_out=False)
            else:
                abort(400)

            posts = pagination.items     # 分页内容
            page = pagination.page       # 当前分页数
            pages = pagination.pages     # 总分页数
            has_prev = pagination.has_prev   # 是否有上一页
            has_next = pagination.has_next   # 是否有下一页

            # 去除post中的content,减少网络流量
            for post in posts:
                post.content = ''

            return {'page': page, 'pages': pages, 'has_prev': has_prev,
                    'has_next': has_next, 'posts': posts}, 200

    # 新增文章
    def post(self):

        args = self.parser.parse_args()
        # 校验参数必须填写
        if args.title is None or args.category is None\
                or args.summary is None or args.content is None:
            abort(400)

        # 文章类型,1是普通文章,2是视频
        if args.post_type is None:
            post_type = '1'
        else:
            post_type = args.post_type

        # 校验用户身份 admin用户允许新增文章
        if args.token is None:
            abort(403)
        user = User.verify_auth_token(args.token)
        if user is None:
            abort(403)
        if user.username != '251319710@qq.com':
            abort(403)

        new_post = Post(user.id, user.nickname, post_type, args.title, args.image,
                        args.category, args.tags, args.summary, args.content)
        db.session.add(new_post)
        db.session.commit()

    # 修改文章
    def put(self, post_id):

        args = self.parser.parse_args()
        # 校验参数必须填写
        if args.post_type is None or args.title is None or args.category is None\
                or args.summary is None or args.content is None:
            abort(400)

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
            post.post_type = args.post_type
            post.title = args.title
            post.image = args.image
            post.category = args.category
            post.summary = args.summary
            post.tags = args.tags
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
            return {'message': '删除成功'}, 204
        else:
            abort(404)
