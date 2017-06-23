#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_pagedown import PageDown     #使用 JavaScript 实现的客户端 Markdown 到 HTML 的转换程序。


# Flask-Login 扩展 :
# 用来管理用户认证系统中的认证状态，且不依赖特定的认证机制。
from  flask_login import LoginManager



bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


#Flask-Login 扩展
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'     #None, basic, strong 提供不同的安全防护等级。strong 会记录用户的IP地址和浏览器的用户代理信息
login_manager.login_view = 'auth.login'           #设置登陆页面的端点。


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    pagedown.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')       #蓝图可以在不同的位置挂载

    return app