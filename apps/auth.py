import random
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, r, db
from flask_mail import Message
from apps.forms import RegisterForm, LoginForm
from models import UserModel
# flask下的通过hash,md5加密方法
from werkzeug.security import generate_password_hash, check_password_hash

# /auth前缀
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('邮箱在数据库中不存在')
                return redirect(url_for('auth.login'))
            if check_password_hash(user.password, password):
                # cookie:
                # cookie不适合存储大量数据,一般用来存放登录授权的东西
                # flask中的session是经过加密后存放在cookie中
                session['user_id'] = user.id
                return redirect('/')
            else:
                print('密码错误')
                return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# GET请求:从服务器上获取数据
# POST请求:将客户端的数据提交给服务器
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码是否正确
        # 表单验证flask-wtf:wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # return redirect(url_for(auth.login))
            return redirect('/auth/login')
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


# 在前端发起请求,不改变当前界面前提下发送请求,使用ajxa技术
@bp.route('/captcha/email')
def get_email_captcha():
    # 使用post传参
    email = request.args.get('email')
    # 4/6位随机数字
    source = random.randint(1000, 9999)
    # 将随机生成的验证码加入redis并设置过期时间
    r.set(email, source)
    r.expire(email, 180)

    # 发送邮件
    message = Message(subject='问答web网页注册验证码', recipients=[email],
                      body='【问答】欢迎使用问答网页端服务，验证码:%d。如非本人操作，请查验账号安全性' % source)
    mail.send(message)

    return jsonify({'code': 200, 'message': '', 'data': None})
