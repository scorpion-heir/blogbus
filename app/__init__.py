from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment 
from config import Config 
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth 
from flask_mail import Mail 




db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
oauth = OAuth()
mail = Mail() 


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config) 
    
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = 'You do not have access to this page. Login first, please!'
    login_manager.login_message_category = 'warning'
    
    

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import bp as auth_bp 
    app.register_blueprint(auth_bp)

    from app.blueprints.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    
    with app.app_context():
        from app.blueprints.main import email 
    

    return app 
