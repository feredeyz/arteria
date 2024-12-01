from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
login_manager = LoginManager()
jwt_manager = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    
    db.init_app(app)
    login_manager.init_app(app)
    jwt_manager.init_app(app)
    
    
    from .routes import auth, profile, main, posts
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(profile)
    app.register_blueprint(posts)
    
    return app