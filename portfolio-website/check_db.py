from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.first()
    if user:
        print(f"Username: {user.username}")
        print(f"Profile photo path: '{user.profile_photo_path}'")
        print(f"Length: {len(user.profile_photo_path)}")
        print(f"Is empty: {not user.profile_photo_path}")
        
        # Update to latest uploaded photo
        latest_photo = "uploads/profile/20251019_171635_1b._Headshot_-_Lake_District_Selfie.jpeg"
        user.profile_photo_path = latest_photo
        db.session.commit()
        print(f"\nUpdated profile photo path to: {latest_photo}")
    else:
        print("No user found in database")
