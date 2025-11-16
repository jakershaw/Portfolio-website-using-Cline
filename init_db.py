"""
Database initialization script for deployment
Creates all tables and initializes admin user if needed
"""
import os
from app import create_app
from app.models import db, User
from config import Config

def init_database():
    """Initialize database with tables and admin user"""
    app = create_app()
    
    with app.app_context():
        # Create all database tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Check if admin user exists
        admin_username = Config.ADMIN_USERNAME
        existing_user = User.query.filter_by(username=admin_username).first()
        
        if not existing_user:
            print(f"Creating admin user: {admin_username}")
            admin_user = User(
                username=admin_username,
                email=Config.ADMIN_EMAIL,
                display_name='Admin User',
                bio_header='Portfolio Administrator',
                bio='',
                linkedin_url='',
                github_url='',
                about_text=''
            )
            admin_user.set_password(Config.ADMIN_PASSWORD)
            db.session.add(admin_user)
            db.session.commit()
            print(f"✓ Admin user '{admin_username}' created successfully")
        else:
            print(f"✓ Admin user '{admin_username}' already exists")
        
        print("\n✓ Database initialization complete!")

if __name__ == '__main__':
    init_database()
