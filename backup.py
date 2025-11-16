"""
Simple backup script for portfolio website
Creates backups of database and uploaded files
"""
import shutil
import os
from datetime import datetime

def create_backup():
    """Create backup of database and uploads folder"""
    
    # Create backups directory if it doesn't exist
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Backup database
    db_file = 'portfolio.db'
    if os.path.exists(db_file):
        backup_db = os.path.join(backup_dir, f'portfolio_{timestamp}.db')
        shutil.copy(db_file, backup_db)
        print(f"✓ Database backed up: {backup_db}")
    else:
        print("⚠ Database file not found, skipping database backup")
    
    # Backup uploads folder
    uploads_dir = 'app/static/uploads'
    if os.path.exists(uploads_dir):
        backup_uploads = os.path.join(backup_dir, f'uploads_{timestamp}')
        shutil.copytree(uploads_dir, backup_uploads)
        print(f"✓ Uploads backed up: {backup_uploads}")
    else:
        print("⚠ Uploads directory not found, skipping uploads backup")
    
    print(f"\n✓ Backup completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backups are stored in: {os.path.abspath(backup_dir)}")
    
    # Clean up old backups (keep last 30 days)
    cleanup_old_backups(backup_dir, days=30)

def cleanup_old_backups(backup_dir, days=30):
    """Remove backups older than specified days"""
    import time
    
    current_time = time.time()
    days_in_seconds = days * 24 * 60 * 60
    
    for item in os.listdir(backup_dir):
        item_path = os.path.join(backup_dir, item)
        if os.path.getmtime(item_path) < (current_time - days_in_seconds):
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"  Removed old backup: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"  Removed old backup folder: {item}")

if __name__ == '__main__':
    print("Starting backup process...")
    create_backup()
