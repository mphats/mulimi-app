#!/usr/bin/env python3
"""
Test Script for Agri AI Backend Setup
This script tests if your Django application is working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_django_setup():
    """Test if Django is properly configured."""
    print("🧪 Testing Django Setup...")
    
    try:
        from django.conf import settings
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ Project name: {settings.ROOT_URLCONF}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        print(f"✅ Allowed hosts: {settings.ALLOWED_HOSTS}")
        return True
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    print("\n🗄️ Testing Database Connection...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        
        if result and result[0] == 1:
            print("✅ Database connection successful!")
            print(f"✅ Database engine: {connection.settings_dict['ENGINE']}")
            print(f"✅ Database name: {connection.settings_dict['NAME']}")
            return True
        else:
            print("❌ Database test query failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_installed_apps():
    """Test if all required apps are installed."""
    print("\n📱 Testing Installed Apps...")
    
    try:
        from django.conf import settings
        
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'rest_framework',
            'api',
            'users',
            'frontend',
            'ai'
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ {app}")
            else:
                print(f"❌ {app} - MISSING!")
                return False
        
        print("✅ All required apps are installed!")
        return True
        
    except Exception as e:
        print(f"❌ App testing error: {e}")
        return False

def test_url_patterns():
    """Test if URL patterns are working."""
    print("\n🔗 Testing URL Patterns...")
    
    try:
        from django.urls import reverse, NoReverseMatch
        
        # Test some basic URLs
        test_urls = [
            ('admin:index', 'Admin'),
            ('api:product-list', 'API Products'),
        ]
        
        for url_name, description in test_urls:
            try:
                url = reverse(url_name)
                print(f"✅ {description}: {url}")
            except NoReverseMatch:
                print(f"⚠️ {description}: URL pattern not found (this might be normal)")
        
        print("✅ URL pattern testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ URL testing error: {e}")
        return False

def test_models():
    """Test if models can be imported."""
    print("\n📊 Testing Models...")
    
    try:
        from api.models import Product, MarketPrice, WeatherData, PestDiagnosis
        from users.models import User
        
        print("✅ Product model imported successfully")
        print("✅ MarketPrice model imported successfully")
        print("✅ WeatherData model imported successfully")
        print("✅ User model imported successfully")
        print("✅ PestDiagnosis model imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Agri AI Backend Setup Test")
    print("=" * 50)
    
    tests = [
        test_django_setup,
        test_database_connection,
        test_installed_apps,
        test_url_patterns,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Visit: http://127.0.0.1:8000/login/")
        print("   2. Test your Flutter app connection")
        print("   3. Create a superuser: python manage.py createsuperuser")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Check your .env file configuration")
        print("   2. Ensure MySQL is running")
        print("   3. Run migrations: python manage.py migrate")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
