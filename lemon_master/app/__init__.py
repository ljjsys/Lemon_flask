from flask import Flask
import pymysql
from flask.ext.sqlalchemy import SQLAlchemy
from config import Config

from flask.ext.login import LoginManager

#####################
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
#login_manager.login_view = 'auth.login'
#####################


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .data_sync import data_sync as data_sync_bluprint
    app.register_blueprint(data_sync_bluprint)

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
