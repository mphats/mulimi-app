#!/usr/bin/env python3
"""
Test Django Server without Celery
This script will start your Django server with minimal configuration
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment variable to use SQLite settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings_sqlite'

# Monkey patch to disable Celery
import django
from django.conf import settings

# Start the Django server
if __name__ == "__main__":
    try:
        django.setup()
        from django.core.management import execute_from_command_line
        print("🚀 Starting Django Server...")
        print("✅ URL: http://127.0.0.1:8000/")
        print("✅ Admin: http://127.0.0.1:8000/admin/")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 50)
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")