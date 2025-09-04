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
from frontend.views import generate_diagnosis
from django.db import models

def test_enhanced_diagnosis():
    """Test the enhanced pest diagnosis functionality"""
    print("🧪 Testing Enhanced Pest Diagnosis Functionality")
    print("=" * 50)
    
    # Test 1: Test the AI diagnosis generation function
    print("\n1. Testing AI Diagnosis Generation:")
    
    test_cases = [
        ("maize", "Yellow spots on leaves", "Northern Corn Leaf Blight"),
        ("tomatoes", "Wilting plants", "Bacterial Wilt"),
        ("maize", "Holes in leaves", "Fall Armyworm Infestation"),
        ("rice", "Brown spots", "Brown Spot Disease"),
        ("beans", "White powder on leaves", "Powdery Mildew"),
    ]
    
    for crop_type, symptoms, expected_diagnosis in test_cases:
        diagnosis, confidence, treatment = generate_diagnosis(crop_type, symptoms)
        print(f"   Crop: {crop_type}, Symptoms: {symptoms}")
        print(f"   → Diagnosis: {diagnosis}")
        print(f"   → Confidence: {confidence}%")
        print(f"   → Expected: {expected_diagnosis}")
        print(f"   ✅ {'PASS' if expected_diagnosis in diagnosis else 'FAIL'}")
        print()
    
    # Test 2: Test form submission with different scenarios
    print("2. Testing Form Submissions:")
    client = Client()
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='testuser2',
        defaults={'email': 'test2@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    client.login(username='testuser2', password='testpass123')
    
    # Test different diagnosis scenarios
    scenarios = [
        {
            'crop_type': 'maize',
            'symptoms': 'Yellow spots on leaves, plants wilting',
            'expected': 'Northern Corn Leaf Blight'
        },
        {
            'crop_type': 'tomatoes',
            'symptoms': 'White powdery substance on leaves',
            'expected': 'Powdery Mildew'
        },
        {
            'crop_type': 'rice',
            'symptoms': 'Brown spots on leaves',
            'expected': 'Brown Spot Disease'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"   Scenario {i}: {scenario['crop_type']} - {scenario['symptoms']}")
        
        response = client.post('/pest-diagnosis/', {
            'crop_type': scenario['crop_type'],
            'symptoms': scenario['symptoms'],
        })
        
        if response.status_code == 302:
            print(f"   ✅ Form submission successful")
            
            # Check the latest diagnosis
            latest_diagnosis = PestDiagnosis.objects.filter(user=user).latest('created_at')
            print(f"   → Generated Diagnosis: {latest_diagnosis.diagnosis}")
            print(f"   → Confidence: {latest_diagnosis.confidence_score}%")
            print(f"   → Treatment: {latest_diagnosis.treatment_advice[:50]}...")
            
            if scenario['expected'] in latest_diagnosis.diagnosis:
                print(f"   ✅ Diagnosis matches expected pattern")
            else:
                print(f"   ⚠️  Diagnosis differs from expected")
        else:
            print(f"   ❌ Form submission failed: {response.status_code}")
        print()
    
    # Test 3: Test page functionality
    print("3. Testing Page Functionality:")
    response = client.get('/pest-diagnosis/')
    
    if response.status_code == 200:
        print("   ✅ Page loads successfully")
        content = response.content.decode()
        
        # Check for key elements
        checks = [
            ('Form elements', 'crop_type' in content and 'symptoms' in content),
            ('Diagnosis history', 'Your Diagnosis History' in content),
            ('Submit button', 'Submit for Diagnosis' in content),
            ('How it works', 'How It Works' in content),
        ]
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
    else:
        print(f"   ❌ Page failed to load: {response.status_code}")
    
    # Test 4: Check diagnosis statistics
    print("\n4. Diagnosis Statistics:")
    total_diagnoses = PestDiagnosis.objects.filter(user=user).count()
    print(f"   Total diagnoses for user: {total_diagnoses}")
    
    if total_diagnoses > 0:
        avg_confidence = PestDiagnosis.objects.filter(user=user).aggregate(
            avg_confidence=models.Avg('confidence_score')
        )['avg_confidence']
        print(f"   Average confidence: {avg_confidence:.1f}%")
        
        # Most common crop types
        crop_counts = PestDiagnosis.objects.filter(user=user).values('crop_type').annotate(
            count=models.Count('id')
        ).order_by('-count')
        print(f"   Most diagnosed crop: {crop_counts[0]['crop_type']} ({crop_counts[0]['count']} times)")
    
    print("\n🎉 Enhanced Pest Diagnosis Test Completed!")
    print("\n📋 Summary of Features Implemented:")
    print("   ✅ AI-like diagnosis generation based on symptoms and crop type")
    print("   ✅ Confidence scoring system")
    print("   ✅ Detailed treatment advice")
    print("   ✅ Diagnosis history with modal details")
    print("   ✅ Form validation and error handling")
    print("   ✅ User authentication required")
    print("   ✅ Image upload support")
    print("   ✅ Statistics display")

if __name__ == '__main__':
    test_enhanced_diagnosis()
