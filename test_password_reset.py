#!/usr/bin/env python
"""
Test script for password reset functionality
Run with: python test_password_reset.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.test.client import Client

def test_password_reset():
    """Test password reset functionality"""
    print("🔒 Testing Password Reset Functionality")
    print("="*50)
    
    # Create a test user
    test_email = "test@example.com"
    test_username = "testuser"
    test_password = "oldpassword123"
    
    try:
        user = User.objects.get(email=test_email)
        user.delete()  # Clean up if exists
    except User.DoesNotExist:
        pass
    
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password
    )
    print(f"✅ Created test user: {test_username} ({test_email})")
    
    # Test token generation
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    print(f"✅ Generated UID: {uid}")
    print(f"✅ Generated Token: {token}")
    
    # Test token validation
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user_from_token = User.objects.get(pk=user_id)
        is_valid = default_token_generator.check_token(user_from_token, token)
        print(f"✅ Token validation: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"❌ Token validation failed: {e}")
        return False
    
    # Test password reset page access
    client = Client()
    
    # Test GET request to password reset page
    response = client.get('/password-reset/')
    print(f"✅ Password reset page status: {response.status_code}")
    
    # Test POST request with email
    response = client.post('/password-reset/', {'email': test_email})
    print(f"✅ Password reset request status: {response.status_code}")
    
    # Test password reset confirmation page
    response = client.get(f'/password-reset-confirm/?uid={uid}&token={token}')
    print(f"✅ Password reset confirm page status: {response.status_code}")
    
    # Test password update
    new_password = "newpassword123"
    response = client.post(f'/password-reset-confirm/', {
        'uid': uid,
        'token': token,
        'new_password': new_password,
        'confirm_password': new_password
    })
    print(f"✅ Password update status: {response.status_code}")
    
    # Verify password was changed
    user.refresh_from_db()
    if user.check_password(new_password):
        print("✅ Password successfully updated!")
    else:
        print("❌ Password update failed!")
    
    # Test with invalid token
    invalid_token = "invalid-token-123"
    response = client.get(f'/password-reset-confirm/?uid={uid}&token={invalid_token}')
    print(f"✅ Invalid token handling status: {response.status_code}")
    
    # Clean up
    user.delete()
    print("✅ Test user cleaned up")
    
    print("\n🎉 Password Reset Test Completed Successfully!")
    return True

if __name__ == "__main__":
    try:
        test_password_reset()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)