# 配置文件

SECRET_KEY = 'santidadday'

# 数据库配置
# MySQL所在的主机名
HOSTNAME = 'localhost'
# MySQL监听的端口号,默认3306
PORT = '3306'
# 连接MySQL的用户名
USERNAME = 'root'
# 连接MySQL的密码
PASSWORD = 'log520='
# MySQL上创建的数据库名称
DATABASE = 'oa'

DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URL

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '1393399898@qq.com'  # 邮箱账号
MAIL_PASSWORD = 'wuzahjkwujzbggba'  # 开启SMTP的授权码
MAIL_DEFAULT_SENDER = '1393399898@qq.com'  # 邮箱账号
