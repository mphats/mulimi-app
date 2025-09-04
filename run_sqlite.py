#!/usr/bin/env python3
"""
Run Django Server with SQLite Configuration
This script will start your Django server with SQLite database
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment variable to use SQLite settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings_sqlite'

print("🚀 Starting Django Server with SQLite...")
print("✅ Database: SQLite (db.sqlite3)")
print("✅ URL: http://127.0.0.1:8000/")
print("✅ Admin: http://127.0.0.1:8000/admin/")
print("✅ Login: http://127.0.0.1:8000/login/")
print("✅ Register: http://127.0.0.1:8000/register/")
print("\n📱 Your Flutter app can connect to these endpoints!")
print("\nPress Ctrl+C to stop the server")
print("=" * 60)

# Start the Django server
if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver'])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 Try running: python manage.py runserver")
