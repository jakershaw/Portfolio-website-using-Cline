from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    display_name = db.Column(db.String(100), default='')
    bio_header = db.Column(db.String(200), default='')
    profile_photo_path = db.Column(db.String(200), default='')
    bio = db.Column(db.Text, default='')
    linkedin_url = db.Column(db.String(200), default='')
    github_url = db.Column(db.String(200), default='')
    about_text = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Project(db.Model):
    """Project model for portfolio items"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Markdown content
    github_url = db.Column(db.String(200), default='')
    image_path = db.Column(db.String(200), default='')
    content_images = db.Column(db.Text, default='[]')  # JSON array of content image paths
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Project {self.title}>'
