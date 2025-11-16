"""
Database migration script to add display_name and bio_header fields
Run this once to update your existing database
"""
from app import create_app, db
from app.models import User

def migrate():
    app = create_app()
    
    with app.app_context():
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        # Add display_name if missing
        if 'display_name' not in columns:
            print("Adding display_name column...")
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE user ADD COLUMN display_name VARCHAR(100) DEFAULT ''"))
                conn.commit()
            print("✓ Added display_name column")
        else:
            print("✓ display_name column already exists")
        
        # Add bio_header if missing
        if 'bio_header' not in columns:
            print("Adding bio_header column...")
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE user ADD COLUMN bio_header VARCHAR(200) DEFAULT ''"))
                conn.commit()
            print("✓ Added bio_header column")
        else:
            print("✓ bio_header column already exists")
        
        # Display current user info
        user = User.query.first()
        if user:
            print(f"\nCurrent user info:")
            print(f"  Username: {user.username}")
            print(f"  Display Name: '{user.display_name}'")
            print(f"  Bio Header: '{user.bio_header}'")
            print(f"  Email: {user.email}")
            print(f"\nYou can now edit these fields in Admin → Edit Profile!")
        else:
            print("\nNo user found in database")

if __name__ == '__main__':
    migrate()
