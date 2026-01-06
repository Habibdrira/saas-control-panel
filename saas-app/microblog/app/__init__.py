import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)

    # =====================
    # CONFIGURATION
    # =====================
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # =====================
    # INIT EXTENSIONS
    # =====================
    db.init_app(app)
    login.init_app(app)

    # =====================
    # TRANSLATION FIX (_)
    # =====================
    @app.context_processor
    def inject_translation():
        return dict(_=lambda x: x)

    # =====================
    # BLUEPRINTS
    # =====================
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # =====================
    # LOGGING
    # =====================
    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog startup")

    return app
