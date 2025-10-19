# Portfolio Website

A minimal, personal portfolio website built with Flask to showcase coding projects and professional information.

## Features

- 🏠 Landing page with profile photo and bio
- 📁 Project showcase with individual project pages
- 📝 Markdown support for project content
- 👤 About/Resume page
- 🔐 Secure admin authentication
- ✏️ Admin panel to edit profile and manage projects
- 📱 Responsive design with Bootstrap 5
- 🔗 Social links (Email, LinkedIn, GitHub) in footer
- 🖼️ Image upload for profile and projects
- 💾 Database-backed content storage

## Technology Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Werkzeug password hashing
- **Content**: Markdown rendering with markdown2

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Clone or Navigate to the Repository

```bash
cd portfolio-website
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Copy the example environment file and edit it:

```bash
copy .env.example .env
```

Edit `.env` and set your credentials:

```
SECRET_KEY=your-secret-key-here
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///portfolio.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password
ADMIN_EMAIL=your-email@example.com
LINKEDIN_URL=https://linkedin.com/in/yourprofile
GITHUB_URL=https://github.com/yourusername
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Initialize Database

```bash
flask init-db
```

This creates the database and admin user with credentials from your `.env` file.

## Running the Application

### Development Server

```bash
python run.py
```

The website will be available at: `http://localhost:5000`

### First Login

1. Navigate to `http://localhost:5000`
2. Click the **Login** button in the top-right
3. Enter the username and password from your `.env` file
4. You'll be redirected to the Admin Dashboard

## Using the Admin Panel

### Edit Profile
1. Go to Admin Dashboard → **Edit Profile**
2. Upload a profile photo
3. Write your bio
4. Add your email and social media links
5. Click **Update Profile**

### Create a Project
1. Go to Admin Dashboard → **Create Project**
2. Enter project title and description
3. Write project content in Markdown
4. Add GitHub repository URL (optional)
5. Upload a project image
6. Check "Published" to make it visible
7. Click **Save Project**

### Manage Projects
- View all projects in the Admin Dashboard
- Click **Edit** to modify a project
- Click **View** to see the public project page
- Use the **Delete** button to remove projects

## Backup Strategy

### Manual Backup

Run the backup script anytime:

```bash
python backup.py
```

This creates timestamped backups of:
- Database file (`portfolio.db`)
- Uploaded files (`app/static/uploads/`)

Backups are stored in the `backups/` folder and automatically cleaned up after 30 days.

### Recommended Schedule

- **Weekly**: Run `python backup.py`
- **Before major changes**: Always create a backup
- **External backup**: Copy the `backups/` folder to an external drive or cloud storage

## Project Structure

```
portfolio-website/
├── app/
│   ├── __init__.py          # App initialization
│   ├── models.py            # Database models
│   ├── routes.py            # URL routes
│   ├── forms.py             # WTForms
│   ├── static/
│   │   ├── css/             # Custom styles
│   │   ├── js/              # JavaScript
│   │   └── uploads/         # Uploaded images
│   └── templates/           # HTML templates
├── migrations/              # Database migrations
├── backups/                 # Backup files (not in Git)
├── .env                     # Environment variables (not in Git)
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
├── backup.py               # Backup script
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── README.md               # This file
```

## Security Best Practices

✅ **Implemented:**
- Password hashing with bcrypt
- CSRF protection on all forms
- Environment variables for secrets
- `.gitignore` excludes sensitive files
- Session management with Flask-Login
- Secure file upload validation

⚠️ **Important:**
- Never commit `.env` file to Git
- Use strong passwords for admin account
- Change `SECRET_KEY` in production
- Keep dependencies updated

## Troubleshooting

### Database Issues

**Reset database:**
```bash
# Delete the database file
del portfolio.db

# Reinitialize
flask init-db
```

### Port Already in Use

Change the port in `run.py`:
```python
app.run(debug=True, port=5001)
```

### Import Errors

Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

## Future Deployment

When ready to deploy online, consider these free options:

1. **PythonAnywhere** (Free tier available)
2. **Render.com** (Free tier available)
3. **Railway** (Free tier with limits)

For production:
- Set `FLASK_ENV=production` in `.env`
- Use a production WSGI server (Gunicorn)
- Consider upgrading to PostgreSQL
- Use environment-specific configuration

## License

This project is for personal use.

## Support

For issues or questions, refer to Flask documentation:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
