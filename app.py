from flask import Flask, session, g
import config
from exts import db, mail
from apps.qa import bp as qa_bp
from apps.auth import bp as auth_bp
from flask_migrate import Migrate
from models import UserModel

app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)
# 将app与数据库、邮箱等相关连接
db.init_app(app)
mail.init_app(app)
# flask迁移ORM模型
migrate = Migrate(app, db)

# 绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# before_request/before_first_request/after_request
# hook中途插入任务
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run()
