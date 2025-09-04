"""
SQLite Configuration for Agri AI Backend
Use this for immediate testing and development
"""

from .settings import *

# Override database settings to use SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Update allowed hosts for local development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.0.2.2', '*']

# Disable Celery for local development
CELERY_TASK_ALWAYS_EAGER = True

# Remove Celery apps for testing
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in [
    'rest_framework_simplejwt.token_blacklist',
    'ai'
]]

print("✅ Using SQLite database for development")
print("✅ Celery disabled for testing")