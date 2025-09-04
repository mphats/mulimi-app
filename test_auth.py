#!/usr/bin/env python3
"""
Simple Authentication Test Script
Tests user registration and login functionality
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

def test_user_creation():
    """Test user creation functionality."""
    print("🧪 Testing User Creation...")
    
    try:
        from django.contrib.auth.models import User
        from users.models import Profile
        
        # Check if test user exists
        test_username = 'testuser123'
        if User.objects.filter(username=test_username).exists():
            print(f"✅ Test user '{test_username}' already exists")
            return True
        
        # Create test user
        user = User.objects.create_user(
            username=test_username,
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Create profile
        profile = Profile.objects.create(user=user, role='FARMER')
        
        print(f"✅ Test user '{test_username}' created successfully")
        print(f"   User ID: {user.id}")
        print(f"   Profile Role: {profile.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ User creation error: {e}")
        return False

def test_authentication():
    """Test user authentication."""
    print("\n🔐 Testing User Authentication...")
    
    try:
        from django.contrib.auth import authenticate
        
        # Test authentication
        user = authenticate(username='testuser123', password='testpass123')
        
        if user is not None:
            print(f"✅ Authentication successful for user: {user.username}")
            print(f"   User ID: {user.id}")
            print(f"   Is Active: {user.is_active}")
            return True
        else:
            print("❌ Authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
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
            print(f"   Database engine: {connection.settings_dict['ENGINE']}")
            print(f"   Database name: {connection.settings_dict['NAME']}")
            return True
        else:
            print("❌ Database test query failed")
            return False
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Authentication System Test")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_user_creation,
        test_authentication
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
        print("🎉 All tests passed! Your authentication system is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Visit: http://127.0.0.1:8000/register/")
        print("   2. Create a new user account")
        print("   3. Test login at: http://127.0.0.1:8000/login/")
        print("   4. Connect your Flutter app")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
