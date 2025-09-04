#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_sqlite')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from api.models import PestDiagnosis

def test_pest_diagnosis_page():
    """Test the pest diagnosis page functionality"""
    client = Client()
    
    # Test 1: Access without authentication (should redirect to login)
    print("Testing pest diagnosis page without authentication...")
    response = client.get('/pest-diagnosis/')
    print(f"Status code: {response.status_code}")
    if response.status_code == 302:
        print("✅ Correctly redirects to login when not authenticated")
    else:
        print("❌ Should redirect to login when not authenticated")
    
    # Test 2: Create a test user and authenticate
    print("\nCreating test user...")
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("✅ Test user created")
    else:
        print("✅ Test user already exists")
    
    # Test 3: Login and access the page
    print("\nTesting pest diagnosis page with authentication...")
    client.login(username='testuser', password='testpass123')
    response = client.get('/pest-diagnosis/')
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Pest diagnosis page loads successfully")
        
        # Check if template is used
        if 'pest_diagnosis.html' in [t.name for t in response.templates]:
            print("✅ Correct template is used")
        else:
            print("❌ Template not found in response")
            
        # Check if form is present
        if 'form' in response.content.decode() or 'crop_type' in response.content.decode():
            print("✅ Form elements are present")
        else:
            print("❌ Form elements not found")
    else:
        print("❌ Pest diagnosis page failed to load")
    
    # Test 4: Test form submission
    print("\nTesting form submission...")
    with open('test_image.txt', 'w') as f:
        f.write('fake image content')
    
    with open('test_image.txt', 'rb') as f:
        response = client.post('/pest-diagnosis/', {
            'crop_type': 'maize',
            'symptoms': 'Yellow spots on leaves, wilting',
        }, files={'image': f})
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 302:
        print("✅ Form submission successful (redirect)")
        
        # Check if diagnosis was created
        diagnoses = PestDiagnosis.objects.filter(user=user)
        if diagnoses.exists():
            print(f"✅ Diagnosis record created: {diagnoses.count()} records")
        else:
            print("❌ No diagnosis record created")
    else:
        print("❌ Form submission failed")
    
    # Clean up
    if os.path.exists('test_image.txt'):
        os.remove('test_image.txt')
    
    print("\n🎉 Pest diagnosis page test completed!")

if __name__ == '__main__':
    test_pest_diagnosis_page()
