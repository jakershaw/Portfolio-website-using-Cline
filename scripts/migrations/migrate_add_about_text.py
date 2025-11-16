"""
Migration script to add about_text field to User model
Run this script to update the database schema
"""
import sys
import os

# Add the parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def migrate():
    """Add about_text column to User table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            if 'about_text' in columns:
                print("✓ about_text column already exists in User table")
                return
            
            # Add the about_text column
            print("Adding about_text column to User table...")
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE user ADD COLUMN about_text TEXT DEFAULT ""'))
                conn.commit()
            
            print("✓ Successfully added about_text column to User table")
            
            # Optionally set default content for existing user
            user = User.query.first()
            if user and not user.about_text:
                default_text = """Hi, I'm James - this is my personal page where I showcase projects I've worked on to build my technical skills.

My career background is primarily in finance but I've always enjoyed learning about and creating more technical projects. My Masters degree in Engineering and past experience working in a Data Science Consultancy have been very helpful in that respect!

In addition to coding projects I also write, produce and perform songs (original songs and covers), so some of the projects showcased relate to the technical aspects of that - see one of my live performances below!

https://www.youtube.com/watch?v=Uc56ojLlkio"""
                user.about_text = default_text
                db.session.commit()
                print("✓ Set default about_text content for existing user")
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            raise

if __name__ == '__main__':
    migrate()
    print("\nMigration completed successfully!")
