from app import create_app, db
from app.models import User
from config import Config

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database and create admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first()
        
        if not admin:
            # Create admin user
            admin = User(
                username=Config.ADMIN_USERNAME,
                email=Config.ADMIN_EMAIL
            )
            admin.set_password(Config.ADMIN_PASSWORD)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✓ Database initialized successfully!")
            print(f"✓ Admin user created: {Config.ADMIN_USERNAME}")
            print(f"  You can now login with the credentials from your .env file")
        else:
            print(f"✓ Database already initialized")
            print(f"✓ Admin user exists: {Config.ADMIN_USERNAME}")

if __name__ == '__main__':
    app.run(debug=True)
