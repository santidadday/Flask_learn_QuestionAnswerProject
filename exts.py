# 扩展文件
# 文件存在的意义是解决循环引用问题
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from redis import StrictRedis

db = SQLAlchemy()
mail = Mail()
r = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
