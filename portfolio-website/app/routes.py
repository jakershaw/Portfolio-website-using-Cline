import os
import json
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import Markup
from werkzeug.utils import secure_filename
from app.models import db, User, Project
from app.forms import LoginForm, ProfileForm, ProjectForm
import markdown2

main = Blueprint('main', __name__)


def convert_bullets_to_markdown(text):
    """
    Text passes through as-is since we use standard Markdown.
    Note: When pasting from Word into a web browser, tabs and special 
    formatting are automatically stripped by the browser.
    """
    return text


def embed_youtube_videos(text):
    """
    Convert YouTube URLs to embedded iframes.
    Supports URLs like: https://www.youtube.com/watch?v=VIDEO_ID
    """
    if not text:
        return text
    
    # Pattern to match YouTube URLs
    youtube_pattern = r'https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)'
    
    def replace_with_iframe(match):
        video_id = match.group(1)
        iframe = f'''<div class="youtube-embed">
    <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/{video_id}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
</div>'''
        return iframe
    
    # Replace YouTube URLs with iframes
    result = re.sub(youtube_pattern, replace_with_iframe, text)
    return Markup(result)


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
        
        # Return path with forward slashes for web compatibility
        web_path = os.path.join('uploads', folder, filename).replace('\\', '/')
        return web_path
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
    # Process about_text to embed YouTube videos
    about_html = embed_youtube_videos(user.about_text) if user and user.about_text else ''
    return render_template('about.html', user=user, about_html=about_html)


@main.route('/project/<int:id>')
def project(id):
    """Individual project page"""
    user = User.query.first()
    project = Project.query.get_or_404(id)
    
    # Convert various bullet formats to markdown, then convert to HTML
    if project.content:
        converted_content = convert_bullets_to_markdown(project.content)
        project_html = markdown2.markdown(converted_content)
        # Embed YouTube videos in project content
        project_html = embed_youtube_videos(project_html)
    else:
        project_html = ''
    
    return render_template('project.html', user=user, project=project, project_html=project_html)


# Authentication
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.admin_dashboard'))
    
    user = User.query.first()
    form = LoginForm()
    if form.validate_on_submit():
        user_account = User.query.filter_by(username=form.username.data).first()
        if user_account and user_account.check_password(form.password.data):
            login_user(user_account)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', user=user, form=form)


@main.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    return redirect(url_for('main.index'))


# Admin routes
@main.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    user = User.query.first()
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/dashboard.html', user=user, projects=projects)


@main.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit profile information"""
    user = User.query.first()
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.display_name = form.display_name.data
        current_user.bio_header = form.bio_header.data
        current_user.bio = form.bio.data
        current_user.about_text = form.about_text.data
        current_user.email = form.email.data
        current_user.linkedin_url = form.linkedin_url.data
        current_user.github_url = form.github_url.data
        
        # Handle profile photo upload
        if form.profile_photo.data and hasattr(form.profile_photo.data, 'filename') and form.profile_photo.data.filename:
            photo_path = save_file(form.profile_photo.data, 'profile')
            if photo_path:
                current_user.profile_photo_path = photo_path
        
        db.session.commit()
        return redirect(url_for('main.edit_profile'))
    
    # Pre-populate form
    form.display_name.data = current_user.display_name
    form.bio_header.data = current_user.bio_header
    form.bio.data = current_user.bio
    form.about_text.data = current_user.about_text
    form.email.data = current_user.email
    form.linkedin_url.data = current_user.linkedin_url
    form.github_url.data = current_user.github_url
    
    return render_template('admin/edit_profile.html', user=user, form=form)


@main.route('/admin/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    """Create new project"""
    user = User.query.first()
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
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            image_path = save_file(form.image.data, 'projects')
            if image_path:
                project.image_path = image_path
        
        # Handle content images upload
        content_image_paths = []
        if form.content_images.data:
            for img_file in form.content_images.data:
                if img_file and hasattr(img_file, 'filename') and img_file.filename:
                    img_path = save_file(img_file, 'projects/content')
                    if img_path:
                        content_image_paths.append(img_path)
        
        project.content_images = json.dumps(content_image_paths)
        
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.project', id=project.id))
    
    # Set published to True by default
    form.published.data = True
    
    return render_template('admin/project_form.html', user=user, form=form, title='New Project')


@main.route('/admin/project/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """Edit existing project"""
    user = User.query.first()
    project = Project.query.get_or_404(id)
    form = ProjectForm()
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.content = form.content.data
        project.github_url = form.github_url.data
        project.published = form.published.data
        
        # Handle image upload
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            image_path = save_file(form.image.data, 'projects')
            if image_path:
                project.image_path = image_path
        
        # Handle content images upload
        if form.content_images.data:
            # Get existing content images
            try:
                existing_images = json.loads(project.content_images) if project.content_images else []
            except (json.JSONDecodeError, TypeError):
                existing_images = []
            
            # Add new content images
            for img_file in form.content_images.data:
                if img_file and hasattr(img_file, 'filename') and img_file.filename:
                    img_path = save_file(img_file, 'projects/content')
                    if img_path:
                        existing_images.append(img_path)
            
            project.content_images = json.dumps(existing_images)
        
        db.session.commit()
        return redirect(url_for('main.project', id=project.id))
    
    # Pre-populate form only on GET request
    if request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.content.data = project.content
        form.github_url.data = project.github_url
        form.published.data = project.published
    
    # Always pass fresh project data from database
    db.session.refresh(project)
    return render_template('admin/project_form.html', user=user, form=form, title='Edit Project', project=project)


@main.route('/admin/project/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.admin_dashboard'))


@main.route('/admin/project/<int:project_id>/delete-image/<path:image_path>')
@login_required
def delete_content_image(project_id, image_path):
    """Delete a content image from a project"""
    project = Project.query.get_or_404(project_id)
    
    try:
        # Get existing images
        existing_images = json.loads(project.content_images) if project.content_images else []
        
        # Remove the specified image from the list
        if image_path in existing_images:
            existing_images.remove(image_path)
            project.content_images = json.dumps(existing_images)
            db.session.commit()
            
            # Delete the physical file
            try:
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], '..', 'static', image_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Could not delete file: {e}")
            
            pass
        else:
            pass
    except Exception as e:
        pass
    
    return redirect(url_for('main.edit_project', id=project_id))


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
