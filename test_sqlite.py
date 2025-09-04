#!/usr/bin/env python3
"""
Test Script for SQLite Configuration
This will test the system with SQLite database
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django environment with SQLite settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_sqlite')
django.setup()

def test_sqlite_setup():
    """Test SQLite setup."""
    print("🧪 Testing SQLite Setup...")
    
    try:
        from django.conf import settings
        from django.db import connection
        
        print(f"✅ Django version: {django.get_version()}")
        print(f"✅ Database engine: {connection.settings_dict['ENGINE']}")
        print(f"✅ Database name: {connection.settings_dict['NAME']}")
        print(f"✅ Debug mode: {settings.DEBUG}")
        
        return True
    except Exception as e:
        print(f"❌ SQLite setup error: {e}")
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
            return True
        else:
            print("❌ Database test query failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
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

def create_test_data():
    """Create test data."""
    print("\n🧪 Creating Test Data...")
    
    try:
        from django.contrib.auth.models import User
        from users.models import Profile
        from api.models import Product, MarketPrice, CommunityPost
        
        # Create test user
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            Profile.objects.create(user=user, role='FARMER')
            print("✅ Test user created: testuser / testpass123")
        else:
            print("✅ Test user already exists: testuser / testpass123")
        
        # Create sample products
        if Product.objects.count() == 0:
            user = User.objects.get(username='testuser')
            Product.objects.create(
                seller=user,
                name='Fresh Tomatoes',
                category='VEGETABLES',
                description='Fresh red tomatoes from local farm',
                quantity=50,
                unit='KG',
                price_per_unit=2.50,
                location='Blantyre',
                contact_phone='+265123456789'
            )
            print("✅ Sample product created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 SQLite Configuration Test")
    print("=" * 50)
    
    tests = [
        test_sqlite_setup,
        test_database_connection,
        test_models,
        create_test_data
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
        print("🎉 All tests passed! Your system is working with SQLite!")
        print("\n📝 Access Your System:")
        print("   1. Admin Panel: http://127.0.0.1:8000/admin/")
        print("   2. Login Page: http://127.0.0.1:8000/login/")
        print("   3. Register Page: http://127.0.0.1:8000/register/")
        print("   4. Home Page: http://127.0.0.1:8000/")
        print("\n🧪 Test Account:")
        print("   Username: testuser")
        print("   Password: testpass123")
        print("\n📱 Flutter App:")
        print("   Your Flutter app is ready to connect!")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
