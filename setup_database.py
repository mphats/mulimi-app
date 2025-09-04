#!/usr/bin/env python
"""
Database Setup Script for Agri AI Django Backend
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e.stderr.strip()}")
        return False

def main():
    """Main setup function."""
    print("🚀 Agri AI Django Backend - Database Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Step 1: Create migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    # Step 2: Apply migrations
    if not run_command("python manage.py migrate", "Applying migrations"):
        sys.exit(1)
    
    # Step 3: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Step 4: Create superuser
    print("\n👤 Creating superuser account...")
    create_superuser = "python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@mlimiapp.com', 'Admin123!') if not User.objects.filter(username='admin').exists() else None\""
    if not run_command(create_superuser, "Creating superuser"):
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("Next steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/")
    print("3. Login with: admin / Admin123!")
    print("4. View API documentation: http://127.0.0.1:8000/api/docs/")

if __name__ == '__main__':
    main()
