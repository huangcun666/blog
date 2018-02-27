from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
import re,flask_whooshalchemyplus

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def filterimg(name):
    repp=re.compile('<img.*?>')
    img=repp.search(name)
    if img:
        img=img.group(0)
    return img

def filterimg2(string):
    rep=re.compile('>(.*?)<')
    string1=''
    for str in rep.findall(string):
        string1+=str
    rep1=re.compile('><')
    string1=rep1.sub('',string1)
    rep2=re.compile('\s')
    string1 = rep2.sub('', string1)
    string1=string1[:115]+'...'
    return string1

def filterimg3(string):
    rep=re.compile('>(.*?)<')
    string1=''
    for str in rep.findall(string):
        string1+=str
    rep1=re.compile('><')
    string1=rep1.sub('',string1)
    rep2=re.compile('\s')
    string1 = rep2.sub('', string1)
    string1=string1[:220]+'...'
    return string1

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    flask_whooshalchemyplus.init_app(app)
    env=app.jinja_env
    env.filters['filterimg']=filterimg
    env.filters['filterimg2']=filterimg2
    env.filters['filterimg3'] = filterimg3

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
