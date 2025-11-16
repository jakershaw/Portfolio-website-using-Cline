@echo off
echo ========================================
echo Starting Portfolio Website Server
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit
)

echo.
echo Installing/updating required packages...
python -m pip install --quiet Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Flask-Migrate==4.0.5 Flask-WTF==1.2.1 python-dotenv==1.0.0 markdown2==2.4.12

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    echo Try running as administrator
    pause
    exit
)

echo.
echo Initializing database...
python -c "from app import create_app, db; from app.models import User; from config import Config; app = create_app(); app.app_context().push(); db.create_all(); admin = User.query.filter_by(username=Config.ADMIN_USERNAME).first(); admin = admin or User(username=Config.ADMIN_USERNAME, email=Config.ADMIN_EMAIL); admin.set_password(Config.ADMIN_PASSWORD) if not admin.id else None; db.session.add(admin); db.session.commit(); print('Database ready!')"

echo.
echo Starting Flask server...
echo.
echo ========================================
echo Your website is now available at:
echo.
echo    http://localhost:5000
echo.
echo Login credentials:
echo    Username: admin  
echo    Password: ChangeThisPassword123!
echo.
echo IMPORTANT: Keep this window open!
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python run.py

echo.
echo Server has stopped.
pause
