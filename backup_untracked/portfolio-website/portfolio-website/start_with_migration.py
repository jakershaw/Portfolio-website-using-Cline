"""
Startup script that runs migration before starting the server
"""
import os
import sys
import subprocess

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_migration():
    """Run the migration script"""
    print("Checking database migration...")
    print("=" * 60)
    
    try:
        # Import and run migration
        from migrate_add_content_images import migrate_database
        migrate_database()
    except Exception as e:
        print(f"Migration check completed (may have already run): {e}")
    
    print("=" * 60)
    print()

def start_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    try:
        subprocess.run([sys.executable, 'run.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == '__main__':
    # Run migration first
    run_migration()
    
    # Then start server
    start_server()
