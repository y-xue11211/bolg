from flask import Blueprint, render_template, url_for

from back.model import Article, ArticleType

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/')
def index():
    arts = Article.query.all()
    return render_template('web/index.html', arts=arts)


@web_blue.route('/about/')
def about():
    return render_template('web/about.html')


@web_blue.route('/message/')
def message():
    return render_template('web/gbook.html')


@web_blue.route('/info/<int:id>')
def info(id):
    art = Article.query.get(id)
    return render_template('web/info.html', art=art)


@web_blue.route('/learn/')
def learning():
    types = ArticleType.query.all()
    arts = Article.query.all()
    print(types)
    return render_template('web/learn.html', types=types, arts=arts)
