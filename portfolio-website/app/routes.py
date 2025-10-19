import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, User, Project
from app.forms import LoginForm, ProfileForm, ProjectForm
import markdown2

main = Blueprint('main', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_file(file, folder=''):
    """Save uploaded file and return path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid overwriting
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return os.path.join('uploads', folder, filename)
    return None


# Public routes
@main.route('/')
def index():
    """Landing page with projects"""
    user = User.query.first()
    projects = Project.query.filter_by(published=True).order_by(Project.created_at.desc()).all()
    return render_template('index.html', user=user, projects=projects)


@main.route('/about')
def about():
    """About/Resume page"""
    user = User.query.first()
    return render_template('about.html', user=user)


@main.route('/project/<int:id>')
def project(id):
    """Individual project page"""
    user = User.query.first()
    project = Project.query.get_or_404(id)
    
    # Convert markdown to HTML
    project_html = markdown2.markdown(project.content)
    
    return render_template('project.html', user=user, project=project, project_html=project_html)


# Authentication
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('main.index'))


# Admin routes
@main.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/dashboard.html', projects=projects)


@main.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit profile information"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.email = form.email.data
        current_user.linkedin_url = form.linkedin_url.data
        current_user.github_url = form.github_url.data
        
        # Handle profile photo upload
        if form.profile_photo.data:
            photo_path = save_file(form.profile_photo.data, 'profile')
            if photo_path:
                current_user.profile_photo_path = photo_path
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.edit_profile'))
    
    # Pre-populate form
    form.bio.data = current_user.bio
    form.email.data = current_user.email
    form.linkedin_url.data = current_user.linkedin_url
    form.github_url.data = current_user.github_url
    
    return render_template('admin/edit_profile.html', form=form)


@main.route('/admin/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    """Create new project"""
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            github_url=form.github_url.data,
            published=form.published.data
        )
        
        # Handle image upload
        if form.image.data:
            image_path = save_file(form.image.data, 'projects')
            if image_path:
                project.image_path = image_path
        
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    # Set published to True by default
    form.published.data = True
    
    return render_template('admin/project_form.html', form=form, title='New Project')


@main.route('/admin/project/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """Edit existing project"""
    project = Project.query.get_or_404(id)
    form = ProjectForm()
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.content = form.content.data
        project.github_url = form.github_url.data
        project.published = form.published.data
        
        # Handle image upload
        if form.image.data:
            image_path = save_file(form.image.data, 'projects')
            if image_path:
                project.image_path = image_path
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    
    # Pre-populate form
    form.title.data = project.title
    form.description.data = project.description
    form.content.data = project.content
    form.github_url.data = project.github_url
    form.published.data = project.published
    
    return render_template('admin/project_form.html', form=form, title='Edit Project', project=project)


@main.route('/admin/project/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))


# Error handlers
@main.app_errorhandler(404)
def not_found_error(error):
    """404 error handler"""
    user = User.query.first()
    return render_template('404.html', user=user), 404


@main.app_errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    user = User.query.first()
    return render_template('404.html', user=user), 500
