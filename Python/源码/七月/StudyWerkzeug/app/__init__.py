from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



bootStrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    bootStrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .manage import manage as manage_blueprint
    app.register_blueprint(manage_blueprint)

    from .Dictionary import dictionary as dictionary_blueprint
    app.register_blueprint(dictionary_blueprint)

    return app