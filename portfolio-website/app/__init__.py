import json
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from app.models import db, User

login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register custom Jinja2 filters
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Parse JSON string to Python object"""
        if not value:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
