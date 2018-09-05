from . import app, db

'''
***************数据库创建(by lei ge)*******************
1.进入mysql创建数据库<db_name>,root用户登录mysql数据库执行以下语句:
  CREATE DATABASE geektest CHARSET=UTF8
2.在config.py配置数据库连接
3.执行在create_db.py
'''

# ***************创建数据库表*****************
#db.drop_all(app=app)
#db.create_all(app=app)
#db.session.commit()



