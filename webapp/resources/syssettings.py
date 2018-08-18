from flask_restful import Resource, abort, fields, marshal_with
from webapp.models import Syssetting


syssetings_fields = {
    'id': fields.Integer,
    'index_notice': fields.String,
    'video_notice': fields.String,
    'job_notice': fields.String
}


# 暂时实现查询操作，后期实现增加和删除操作
class SyssetingsApi(Resource):

    @marshal_with(syssetings_fields)
    def get(self):
        # 查询所有的分类
        syssetings = Syssetting.query.first()
        if syssetings:
            return syssetings, 200
        else:
            abort(404, message='无系统设定数据')
