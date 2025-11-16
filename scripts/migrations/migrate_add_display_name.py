"""
Database migration script to add display_name field to User model
Run this once to update your existing database
"""
from app import create_app, db
from app.models import User

def migrate():
    app = create_app()
    
    with app.app_context():
        # Check if column already exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        if 'display_name' not in columns:
            print("Adding display_name column to User table...")
            
            # Add the column using raw SQL
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE user ADD COLUMN display_name VARCHAR(100) DEFAULT ''"))
                conn.commit()
            
            print("✓ Successfully added display_name column")
        else:
            print("✓ display_name column already exists")
        
        # Display current user info
        user = User.query.first()
        if user:
            print(f"\nCurrent user info:")
            print(f"  Username: {user.username}")
            print(f"  Display Name: '{user.display_name}'")
            print(f"  Email: {user.email}")
            print(f"\nYou can now set your display name in the Edit Profile page!")
        else:
            print("\nNo user found in database")

if __name__ == '__main__':
    migrate()
