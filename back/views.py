
from flask import Blueprint, render_template, request, url_for, session
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from back.model import User, Article, ArticleType, db
from untils.functions import is_login

back_blue = Blueprint('back', __name__)


# 首页路由
@back_blue.route('/index/')
@is_login      # 判断是否登录
def index():
    return render_template('back/index.html')


# 注册路由
@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 判断注册账号是否满足条件
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已以存在，请重新注册'
                return render_template('back/register.html', error=error)
            else:
                if password2 == password:
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.sava()
                    return redirect(url_for('back.login'))
                else:
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)


# 登录路由
@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断账号密码是否匹配
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在'
                return render_template('back/login.html', error=error)
            if user.is_delete:
                error = '账号被注销'
                return render_template('back/login.html', error=error)
            if not check_password_hash(user.password, password):
                error = '密码错误'
                return render_template('back/login.html', error=error)
            session['user_id'] = user.id
            return redirect(url_for('back.index'))

        else:
            error = '请填写完整信息'
            return render_template('back/login.html', error=error)


# 注销路由
@back_blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    # 退出登录 删除session中user_id的值
    print(session['user_id'])
    del session['user_id']
    return redirect(url_for('back.login'))


# 分类列表路由
@back_blue.route('/a_type/', methods=['GET', 'POST'])
@is_login
def a_type():
    if request.method == 'GET':
        # 定义变量获取所有分类对象，传统给分类列表页面
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


# 添加分类路由
@back_blue.route('/add_type/', methods=['GET', 'POST'])
@is_login
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))
        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


# 删除分类路由
@back_blue.route('/del_type/<int:id>', methods=['GET'])
@is_login
def del_type(id):
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


# 文章分类路由
@back_blue.route('/article_list/', methods=['GET'])
@is_login
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)


# 文章添加路由
@back_blue.route('/article_add/', methods=['GET', 'POST'])
@is_login
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error = '请填写完整文章信息'
            return render_template('back/article_detail.html', error)


# 修改文章路由
@back_blue.route('/alter_art/<int:id>', methods=['GET', 'POST'])
@is_login
def alter_art(id):
    art = Article.query.get(id)
    types = ArticleType.query.all()
    if request.method == 'GET':
        return render_template('back/article_alter.html', art=art, types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        # art = Article()
        art.title = title
        art.desc = desc
        art.content = content
        art.type = category
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('back.article_list'))
    else:
        return render_template('back/article_list.html')


# 删除文章路由
@back_blue.route('/del_art/<int:id>', methods=['GET'])
@is_login
def del_art(id):
    art = Article.query.get(id)
    db.session.delete(art)
    db.session.commit()
    return redirect(url_for('back.article_list'))


# 用户列表路由
@back_blue.route('/user_list/', methods=['GET'])
@is_login
def user_list():
    users = User.query.all()
    return render_template('back/user_list.html', users=users)


# 删除用户路由
@back_blue.route('/del_user/<int:id>', methods=['GET'])
@is_login
def del_user(id):
    user = User.query.get(id)
    user.is_delete = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('back.user_list'))


# 修改密码路由
@back_blue.route('/change_pwd/<int:id>', methods=['GET', 'POST'])
@is_login
def change_pwd(id):
    user = User.query.get(id)
    if request.method == 'GET':
        return render_template('back/change_pwd.html', user=user)
    if request.method == 'POST':
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password and password1 and password2:
            if check_password_hash(user.password, password):
                if password1 == password2:
                    user.password = generate_password_hash(password1)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('back.user_list'))
                else:
                    error = '两次密码不一样，请确认'
                    return render_template('back/change_pwd.html', error=error)
            else:
                error = '原密码错误'
                return render_template('back/change_pwd.html', error=error)
        else:
            error = '请输入完整信息'
            return render_template('back/change_pwd.html', error=error)






