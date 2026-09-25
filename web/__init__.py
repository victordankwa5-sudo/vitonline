from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
import os
from dotenv import load_dotenv
load_dotenv()


db = SQLAlchemy()
DB_NAME = "database.db"

APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
MAIL_SERVER = os.environ.get('APP_MAIL_SERVER')
MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD')

def create_app():
    app = Flask(__name__)
    global mail
    mail = Mail(app)
    app.config['SECRET_KEY'] = APP_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    db.init_app(app)
    
    from.views import views
    from .auth import auth
    from .admin import admin
    from .admin_views import admin_views
    # from .payment import payment
    from .paystack import pay
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(admin_views, url_prefix='/')
    # app.register_blueprint(payment, url_prefix='/')
    app.register_blueprint(pay, url_prefix='/')
    
    from .models import User
    
    with app.app_context():
        create_db()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_db():
    if not path.exists('web/' + DB_NAME):
        db.create_all()