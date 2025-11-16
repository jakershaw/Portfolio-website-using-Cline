# How to Build a Portfolio Website with Flask - Beginner's Guide

**Goal:** Learn to build a complete website from scratch, step by step!  
**Time:** 2-3 hours for beginners  
**Prerequisites:** Basic Python knowledge, Python installed on your computer

---

## Table of Contents

1. [Understanding the Big Picture](#understanding-the-big-picture)
2. [What is Flask?](#what-is-flask)
3. [Project Planning](#project-planning)
4. [Step-by-Step Build Process](#step-by-step-build-process)
5. [Understanding Each Component](#understanding-each-component)
6. [Common Patterns You'll Use](#common-patterns-youll-use)
7. [Learning Resources](#learning-resources)

---

## Understanding the Big Picture

### What We're Building
A personal website where you can:
- Show your projects to visitors
- Login and edit your content
- Store everything in a database

### How Websites Work (Simple Explanation)

```
Browser (You) ←→ Flask Server ←→ Database
                      ↓
                  Templates (HTML)
```

1. **Browser:** What you see (Chrome, Firefox, etc.)
2. **Flask Server:** The "brain" that handles requests
3. **Database:** Where we save information
4. **Templates:** HTML files that become web pages

---

## What is Flask?

**Flask is a "micro web framework" for Python.**

### What Does That Mean?

Think of Flask like LEGO blocks:
- ✅ **Small and simple:** Easy to learn
- ✅ **Flexible:** Build exactly what you need
- ✅ **Python-based:** Use Python skills you already have

### The Flask Request-Response Cycle

```python
# When someone visits your website:
@app.route('/')              # 1. They visit a URL
def index():                 # 2. Flask runs this function
    return render_template()  # 3. Flask sends back HTML
```

It's that simple!

---

## Project Planning

### Step 1: Break Down What You Need

Before writing code, plan your website:

#### Pages Needed:
1. **Home page** - Shows projects
2. **About page** - Your bio
3. **Project detail page** - Individual project info
4. **Login page** - For you to log in
5. **Admin pages** - To edit content

#### Features Needed:
- User can view projects ✓
- Admin can login ✓
- Admin can add/edit projects ✓
- Store data in database ✓

### Step 2: Choose Your Tools

**Backend (Server):**
- Flask - The web framework
- SQLAlchemy - Talk to database easily
- Flask-Login - Handle user sessions

**Frontend (What Users See):**
- Bootstrap - Make it look nice quickly
- HTML/CSS - Structure and style
- Jinja2 - Put Python data into HTML

**Database:**
- SQLite - Simple file-based database (perfect for learning!)

---

## Step-by-Step Build Process

### Phase 1: Project Setup (20 minutes)

#### 1.1 Create Project Structure

```
my-website/
├── app/                 # Your application code
│   ├── __init__.py     # Sets up Flask
│   ├── models.py       # Database tables
│   ├── routes.py       # URL handlers
│   ├── forms.py        # Web forms
│   ├── static/         # CSS, JS, images
│   └── templates/      # HTML files
├── config.py           # Settings
├── run.py             # Start the website
└── requirements.txt   # List of tools needed
```

**Why this structure?**
- **Organized:** Easy to find things
- **Scalable:** Can grow as project grows
- **Standard:** Other developers recognize it

#### 1.2 Create requirements.txt

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
```

**What each does:**
- `Flask` - Core framework
- `Flask-SQLAlchemy` - Database made easy
- `Flask-Login` - Handle who's logged in
- `Flask-WTF` - Create web forms safely

#### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This downloads all the tools you need!

---

### Phase 2: Configuration (10 minutes)

#### 2.1 Create config.py

```python
class Config:
    # Secret key - keeps your site secure
    SECRET_KEY = 'change-this-to-something-random'
    
    # Database location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mysite.db'
```

**What's happening:**
- `SECRET_KEY` - Like a password for your app
- `SQLALCHEMY_DATABASE_URI` - Where to save data

---

### Phase 3: Database Models (30 minutes)

#### 3.1 Understanding Databases

Think of a database like Excel:
- **Tables** = Sheets
- **Columns** = Headers
- **Rows** = Data entries

#### 3.2 Create models.py

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Like a User profile table in Excel"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    bio = db.Column(db.Text)
```

**Breaking it down:**
- `class User` - Creates a "User" table
- `db.Column` - Adds a column to the table
- `primary_key=True` - Makes 'id' unique
- `unique=True` - No duplicate usernames allowed

#### 3.3 Example: What This Creates

| id | username | password | bio |
|----|----------|----------|-----|
| 1  | admin    | hash123  | Hello! |

---

### Phase 4: Flask App Setup (20 minutes)

#### 4.1 Create app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create the Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Import routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app
```

**What's happening:**
1. Create Flask app
2. Load configuration
3. Set up database
4. Connect routes

#### 4.2 Understanding Flask Factory Pattern

```python
# Instead of:
app = Flask(__name__)  # Global variable (harder to test)

# We use:
def create_app():      # Function (better practice)
    app = Flask(__name__)
    return app
```

**Benefits:**
- Can create multiple apps for testing
- Better organized
- Industry standard

---

### Phase 5: Routes (URLs) (40 minutes)

#### 5.1 Create app/routes.py

```python
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/about')
def about():
    """About page"""
    return render_template('about.html')
```

**Understanding Routes:**
- `@main.route('/')` - When user visits "/"
- `def index()` - Run this function
- `render_template()` - Show this HTML

#### 5.2 Route with Parameters

```python
@main.route('/project/<int:id>')
def project(id):
    """Show specific project"""
    project = Project.query.get(id)
    return render_template('project.html', project=project)
```

**What's new:**
- `<int:id>` - Capture number from URL
- `/project/1` → `id=1`
- `/project/2` → `id=2`

#### 5.3 Forms and POST Requests

```python
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # User submitted the form
        username = form.username.data
        password = form.password.data
        # Check if correct...
    
    return render_template('login.html', form=form)
```

**Two methods:**
- `GET` - Show the page
- `POST` - Process form submission

---

### Phase 6: Templates (HTML) (45 minutes)

#### 6.1 Base Template (base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
    <link href="bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation bar -->
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>
    
    <!-- Page content goes here -->
    {% block content %}{% endblock %}
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2025 My Site</p>
    </footer>
</body>
</html>
```

**Jinja2 Syntax:**
- `{% block content %}` - Other pages fill this in
- `{{ variable }}` - Show Python variable
- `{% for item in items %}` - Loop through list

#### 6.2 Child Template (index.html)

```html
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>Welcome!</h1>
    
    {% for project in projects %}
        <div class="project-card">
            <h2>{{ project.title }}</h2>
            <p>{{ project.description }}</p>
        </div>
    {% endfor %}
{% endblock %}
```

**Inheritance:**
- `extends "base.html"` - Use base template
- Override blocks with new content
- Keeps code DRY (Don't Repeat Yourself)

---

### Phase 7: Forms (30 minutes)

#### 7.1 Create app/forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """Login form with validation"""
    username = StringField('Username', 
                          validators=[DataRequired()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    submit = SubmitField('Login')
```

**Form Fields:**
- `StringField` - Text input
- `PasswordField` - Hidden text
- `SubmitField` - Button
- `validators` - Check if data is valid

#### 7.2 Using Forms in Templates

```html
<form method="POST">
    {{ form.hidden_tag() }}  <!-- CSRF protection -->
    
    {{ form.username.label }}
    {{ form.username(class='form-control') }}
    
    {{ form.password.label }}
    {{ form.password(class='form-control') }}
    
    {{ form.submit(class='btn btn-primary') }}
</form>
```

**CSRF Protection:**
- Prevents hackers from faking form submissions
- `hidden_tag()` adds a secret token

---

### Phase 8: Authentication (40 minutes)

#### 8.1 Password Security

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    password_hash = db.Column(db.String(200))
    
    def set_password(self, password):
        """Never store passwords directly!"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
```

**Why hash passwords:**
- If database is stolen, passwords are safe
- Can't reverse a hash
- Industry standard

#### 8.2 Flask-Login Setup

```python
from flask_login import LoginManager, login_user, logout_user, login_required

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login needs this to remember who's logged in"""
    return User.query.get(int(user_id))

@main.route('/admin')
@login_required  # Must be logged in to see this!
def admin():
    return render_template('admin.html')
```

**How it works:**
1. User logs in
2. Flask-Login stores their ID in session
3. `@login_required` checks if they're logged in
4. Automatic redirect if not

---

### Phase 9: Database Operations (30 minutes)

#### 9.1 Create (Add new data)

```python
# Create new project
new_project = Project(
    title='My Project',
    description='Cool stuff'
)
db.session.add(new_project)
db.session.commit()
```

#### 9.2 Read (Get data)

```python
# Get all projects
all_projects = Project.query.all()

# Get one project
project = Project.query.get(1)  # ID = 1

# Filter projects
published = Project.query.filter_by(published=True).all()
```

#### 9.3 Update (Change data)

```python
# Get project
project = Project.query.get(1)

# Change it
project.title = 'New Title'

# Save changes
db.session.commit()
```

#### 9.4 Delete (Remove data)

```python
project = Project.query.get(1)
db.session.delete(project)
db.session.commit()
```

**Remember:** Always `commit()` to save changes!

---

### Phase 10: Static Files (CSS, JS, Images) (20 minutes)

#### 10.1 File Structure

```
app/static/
├── css/
│   └── style.css
├── js/
│   └── main.js
└── uploads/
    └── images/
```

#### 10.2 Linking in Templates

```html
<!-- CSS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">

<!-- JavaScript -->
<script src="{{ url_for('static', filename='js/main.js') }}"></script>

<!-- Image -->
<img src="{{ url_for('static', filename='uploads/photo.jpg') }}">
```

**url_for():**
- Generates correct URL
- Works even if you move files
- Best practice!

---

## Understanding Each Component

### Flask App Structure Explained

```python
# 1. CREATE APP
app = Flask(__name__)

# 2. CONFIGURE
app.config['SECRET_KEY'] = 'secret'

# 3. SETUP DATABASE
db.init_app(app)

# 4. DEFINE ROUTES
@app.route('/')
def index():
    return 'Hello!'

# 5. RUN APP
if __name__ == '__main__':
    app.run(debug=True)
```

### Request-Response Flow

```
User types URL (localhost:5000/about)
    ↓
Flask finds matching route (@app.route('/about'))
    ↓
Runs the function (def about():)
    ↓
Function returns HTML
    ↓
User's browser displays the page
```

---

## Common Patterns You'll Use

### Pattern 1: Show List of Items

```python
@app.route('/projects')
def projects():
    # Get all projects from database
    all_projects = Project.query.all()
    
    # Send to template
    return render_template('projects.html', 
                         projects=all_projects)
```

```html
<!-- In template -->
{% for project in projects %}
    <h2>{{ project.title }}</h2>
{% endfor %}
```

### Pattern 2: Show One Item

```python
@app.route('/project/<int:id>')
def project_detail(id):
    # Get specific project
    project = Project.query.get_or_404(id)
    
    return render_template('project.html', 
                         project=project)
```

### Pattern 3: Handle Form Submission

```python
@app.route('/add', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    
    if form.validate_on_submit():
        # Form was submitted and valid
        new_project = Project(
            title=form.title.data
        )
        db.session.add(new_project)
        db.session.commit()
        
        return redirect(url_for('projects'))
    
    # Show empty form
    return render_template('add.html', form=form)
```

### Pattern 4: File Upload

```python
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        
        # Make filename safe
        filename = secure_filename(file.filename)
        
        # Save file
        file.save(os.path.join('uploads', filename))
    
    return redirect(url_for('index'))
```

---

## Learning Path

### Week 1: Basics
1. **Day 1-2:** Learn Python basics (if needed)
2. **Day 3-4:** Understand HTML/CSS basics
3. **Day 5-7:** Follow Flask tutorial (official docs)

### Week 2: Building
1. **Day 1-2:** Create simple Flask app (Hello World → Form → Database)
2. **Day 3-4:** Add authentication
3. **Day 5-7:** Style with Bootstrap

### Week 3: Features
1. **Day 1-3:** Add file uploads
2. **Day 4-5:** Create admin panel
3. **Day 6-7:** Polish and test

---

## Common Beginner Mistakes (And How to Fix Them)

### Mistake 1: Forgetting db.session.commit()

```python
# WRONG - Changes not saved!
project.title = 'New Title'

# RIGHT - Changes saved!
project.title = 'New Title'
db.session.commit()
```

### Mistake 2: Not Checking if User is Logged In

```python
# WRONG - Anyone can access admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# RIGHT - Only logged-in users
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')
```

### Mistake 3: Storing Passwords in Plain Text

```python
# WRONG - Passwords visible!
user.password = 'secret123'

# RIGHT - Passwords hashed!
user.set_password('secret123')
```

### Mistake 4: Forgetting CSRF Token

```html
<!-- WRONG - Security risk! -->
<form method="POST">
    <input type="text" name="username">
</form>

<!-- RIGHT - Protected! -->
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.username }}
</form>
```

---

## Learning Resources

### Official Documentation
- **Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Bootstrap:** https://getbootstrap.com/

### Tutorials (Beginner-Friendly)
1. **Flask Mega-Tutorial** by Miguel Grinberg (Free!)
   - Most recommended Flask tutorial
   - Step-by-step with explanations

2. **CS50 Web Programming** (Free on YouTube)
   - Harvard course
   - Covers Flask and more

3. **Real Python Flask Tutorials**
   - Clear explanations
   - Lots of examples

### Practice Projects (Start Simple!)
1. **Todo List App** - CRUD operations
2. **Blog** - Posts and comments
3. **Note-Taking App** - File uploads
4. **Portfolio Site** - What we built!

---

## Debugging Tips

### Problem: Page Won't Load

```python
# 1. Check if server is running
# You should see: "Running on http://127.0.0.1:5000"

# 2. Check for errors in terminal

# 3. Check your route
@app.route('/mypage')  # URL must match!
def my_page():
    return render_template('mypage.html')
```

### Problem: Database Error

```python
# Solution 1: Initialize database
with app.app_context():
    db.create_all()

# Solution 2: Check model definition
# Make sure all columns are defined correctly

# Solution 3: Delete database and start fresh
# (Only in development!)
```

### Problem: Template Not Found

```
# Check file location:
app/templates/index.html  ✓ Correct
app/index.html            ✗ Wrong location
templates/index.html      ✗ Outside app folder
```

---

## Next Steps After This Tutorial

### Level Up Your Skills

1. **Add More Features:**
   - Search functionality
   - Pagination (show 10 items per page)
   - Comments system
   - Tags/categories

2. **Improve Design:**
   - Custom CSS
   - Animations
   - Responsive images
   - Dark mode

3. **Deploy Online:**
   - Learn Git/GitHub
   - Choose hosting (Heroku, PythonAnywhere)
   - Get custom domain

4. **Add Testing:**
   - Write tests for your functions
   - Learn pytest
   - Test coverage

5. **Learn More Python Web Dev:**
   - RESTful APIs
   - JavaScript frameworks (React, Vue)
   - Database optimization
   - Caching

---

## Summary: The Journey

### What You Learned
✅ How websites work  
✅ Flask basics  
✅ Database operations  
✅ User authentication  
✅ Form handling  
✅ Template rendering  
✅ File uploads  
✅ Security best practices  

### Skills You Gained
✅ Python web development  
✅ Database design  
✅ HTML/CSS/Bootstrap  
✅ Security awareness  
✅ Problem-solving  

### What's Next?
✅ Build your own projects  
✅ Learn advanced topics  
✅ Join developer community  
✅ Keep coding!  

---

## Remember

**Programming is learned by doing!**

Don't just read - type out the code, make mistakes, fix them, and learn. Every error message is a learning opportunity!

**Start small, build up gradually:**
1. Hello World
2. Show some text
3. Add a form
4. Connect to database
5. Add features one by one

**You've got this! 🚀**

---

## Glossary of Terms

**App/Application** - Your website program  
**Backend** - Server-side code (Python/Flask)  
**Blueprint** - Way to organize routes  
**CRUD** - Create, Read, Update, Delete  
**CSRF** - Cross-Site Request Forgery (security)  
**Database** - Where data is stored  
**Debug Mode** - Shows detailed errors  
**Flask** - Python web framework  
**Frontend** - What users see (HTML/CSS)  
**GET/POST** - HTTP methods  
**Jinja2** - Template engine  
**Migration** - Database schema change  
**Model** - Database table definition  
**ORM** - Object-Relational Mapper  
**Route** - URL handler  
**Session** - Remembers user between requests  
**SQLAlchemy** - Database library  
**Template** - HTML file with placeholders  
**WSGI** - Web Server Gateway Interface  

---

**End of Tutorial - Happy Coding!** 🎉
