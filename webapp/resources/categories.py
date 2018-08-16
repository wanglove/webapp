from flask_restful import Resource, abort, fields, marshal_with
from webapp.models import Category


category_data = {
    'id': fields.Integer,
    'category': fields.String,
    'type': fields.String
}

category_fields = {
    'categories': fields.List(fields.Nested(category_data))   # list返回多条数据
}


class CategoryApi(Resource):

    @marshal_with(category_fields)
    def get(self):
        # 查询所有的分类
        categories = Category.query.order_by(Category.id).all()
        if categories:
            return {'categories': categories}, 200
        else:
            abort(404)
