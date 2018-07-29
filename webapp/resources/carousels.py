from flask_restful import Resource, abort, fields, marshal_with
from webapp.models import Carousel


carousel_data = {
    'id': fields.Integer,
    'postid': fields.Integer,
    'position': fields.String,
    'title': fields.String,
    'image': fields.String,
    'summary': fields.String
}

carousel_fields = {
    'carousels': fields.List(fields.Nested(carousel_data))   # list返回多条数据
}


# 暂时实现查询操作，后期实现增加和删除操作
class CarouselApi(Resource):

    @marshal_with(carousel_fields)
    def get(self):
        # 查询所有的分类
        carousels = Carousel.query.order_by(Carousel.id).all()
        if carousels:
            return {'carousels': carousels}, 200
        else:
            abort(404)

