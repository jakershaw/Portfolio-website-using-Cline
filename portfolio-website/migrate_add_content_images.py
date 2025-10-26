"""
Database Migration Script: Add content_images field to Project model
Run this script to update your existing database with the new content_images field.
"""

import os
import sys

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Project
from sqlalchemy import text

def migrate_database():
    """Add content_images field to Project table if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if the column already exists
            result = db.session.execute(text(
                "SELECT COUNT(*) FROM pragma_table_info('project') WHERE name='content_images'"
            ))
            column_exists = result.scalar() > 0
            
            if column_exists:
                print("✓ content_images column already exists in Project table")
                return
            
            # Add the new column with default value
            print("Adding content_images column to Project table...")
            db.session.execute(text(
                "ALTER TABLE project ADD COLUMN content_images TEXT DEFAULT '[]'"
            ))
            db.session.commit()
            
            print("✓ Migration completed successfully!")
            print("  - Added content_images field to Project model")
            print("\nYou can now upload content images when creating/editing projects.")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Migration failed: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    print("Starting database migration...")
    print("=" * 60)
    migrate_database()
    print("=" * 60)
