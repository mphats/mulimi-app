#!/usr/bin/env python3
"""
Quick Setup Script for Agri AI Backend
This script helps you get the system running quickly.
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

def create_test_data():
    """Create some test data for the system."""
    print("🧪 Creating Test Data...")
    
    try:
        from django.contrib.auth.models import User
        from users.models import Profile
        from api.models import Product, MarketPrice, WeatherData, CommunityPost
        
        # Create test user if it doesn't exist
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
            products = [
                {
                    'name': 'Fresh Tomatoes',
                    'category': 'VEGETABLES',
                    'description': 'Fresh red tomatoes from local farm',
                    'quantity': 50,
                    'unit': 'KG',
                    'price_per_unit': 2.50,
                    'location': 'Blantyre',
                    'contact_phone': '+265123456789'
                },
                {
                    'name': 'Maize',
                    'category': 'GRAINS',
                    'description': 'Quality maize grain',
                    'quantity': 100,
                    'unit': 'KG',
                    'price_per_unit': 1.80,
                    'location': 'Lilongwe',
                    'contact_phone': '+265123456789'
                }
            ]
            
            for product_data in products:
                Product.objects.create(seller=user, **product_data)
            
            print("✅ Sample products created")
        
        # Create sample market prices
        if MarketPrice.objects.count() == 0:
            prices = [
                {
                    'product_category': 'VEGETABLES',
                    'market_name': 'Blantyre Market',
                    'location': 'Blantyre',
                    'price_per_unit': 2.50,
                    'unit': 'KG',
                    'currency': 'MWK'
                },
                {
                    'product_category': 'GRAINS',
                    'market_name': 'Lilongwe Market',
                    'location': 'Lilongwe',
                    'price_per_unit': 1.80,
                    'unit': 'KG',
                    'currency': 'MWK'
                }
            ]
            
            for price_data in prices:
                MarketPrice.objects.create(**price_data)
            
            print("✅ Sample market prices created")
        
        # Create sample community posts
        if CommunityPost.objects.count() == 0:
            user = User.objects.get(username='testuser')
            posts = [
                {
                    'title': 'Best time to plant tomatoes?',
                    'content': 'When is the best time to plant tomatoes in Malawi?',
                    'category': 'PLANTING',
                    'is_question': True
                },
                {
                    'title': 'Organic pest control methods',
                    'content': 'Share your organic pest control methods for vegetables.',
                    'category': 'PEST_CONTROL',
                    'is_question': False
                }
            ]
            
            for post_data in posts:
                CommunityPost.objects.create(author=user, **post_data)
            
            print("✅ Sample community posts created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return False

def show_system_info():
    """Show system information."""
    print("\n📊 System Information:")
    print("=" * 50)
    
    try:
        from django.conf import settings
        from django.db import connection
        
        print(f"✅ Django Version: {django.get_version()}")
        print(f"✅ Database Engine: {connection.settings_dict['ENGINE']}")
        print(f"✅ Database Name: {connection.settings_dict['NAME']}")
        print(f"✅ Debug Mode: {settings.DEBUG}")
        print(f"✅ Allowed Hosts: {settings.ALLOWED_HOSTS}")
        
        # Count objects
        from django.contrib.auth.models import User
        from api.models import Product, MarketPrice, CommunityPost
        from users.models import Profile
        
        print(f"✅ Total Users: {User.objects.count()}")
        print(f"✅ Total Profiles: {Profile.objects.count()}")
        print(f"✅ Total Products: {Product.objects.count()}")
        print(f"✅ Total Market Prices: {MarketPrice.objects.count()}")
        print(f"✅ Total Community Posts: {CommunityPost.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error getting system info: {e}")

def main():
    """Main setup function."""
    print("🚀 Quick Setup for Agri AI Backend")
    print("=" * 50)
    
    # Create test data
    if create_test_data():
        print("\n✅ Test data created successfully!")
    else:
        print("\n⚠️ Some test data creation failed")
    
    # Show system info
    show_system_info()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\n📝 Access Your System:")
    print("   1. Admin Panel: http://127.0.0.1:8000/admin/")
    print("      Username: admin")
    print("      Password: (what you set)")
    print("   2. Login Page: http://127.0.0.1:8000/login/")
    print("   3. Register Page: http://127.0.0.1:8000/register/")
    print("   4. Home Page: http://127.0.0.1:8000/")
    print("\n🧪 Test Account:")
    print("   Username: testuser")
    print("   Password: testpass123")
    print("\n📱 Flutter App:")
    print("   Your Flutter app is ready to connect to these endpoints!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
