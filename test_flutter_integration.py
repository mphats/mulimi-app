#!/usr/bin/env python3
"""
Comprehensive test script for the Mlimi Django backend API.
This script tests all major API endpoints to ensure proper functionality.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

class MlimiAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }

    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.test_results['passed'] += 1
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")

    def make_request(self, method: str, endpoint: str, data: dict = None, 
                    files: dict = None, auth_required: bool = True) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.api_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth_required and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers if auth_required else {})
            elif method == 'POST':
                if files:
                    headers.pop('Content-Type', None)  # Let requests set it for multipart
                    response = requests.post(url, data=data, files=files, headers=headers if auth_required else {})
                else:
                    response = requests.post(url, json=data, headers=headers if auth_required else {})
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            return {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'success': 200 <= response.status_code < 300
            }
        except requests.exceptions.RequestException as e:
            return {
                'status_code': 0,
                'data': {'error': str(e)},
                'success': False
            }
        except json.JSONDecodeError:
            return {
                'status_code': response.status_code,
                'data': {'error': 'Invalid JSON response'},
                'success': False
            }

    def test_health_check(self):
        """Test health check endpoint"""
        print("\n🔍 Testing Health Check...")
        response = self.make_request('GET', '/health', auth_required=False)
        
        self.log_result(
            "Health Check",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_user_registration(self):
        """Test user registration"""
        print("\n🔍 Testing User Registration...")
        
        # Test data
        user_data = {
            'username': f'testuser_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'password': 'testpass123',
            'role': 'FARMER'
        }
        
        response = self.make_request('POST', '/auth/register/', user_data, auth_required=False)
        
        self.log_result(
            "User Registration",
            response['success'],
            f"Status: {response['status_code']}, Data: {response['data']}"
        )
        
        return user_data if response['success'] else None

    def test_user_login(self, username: str, password: str):
        """Test user login"""
        print("\n🔍 Testing User Login...")
        
        login_data = {
            'username': username,
            'password': password
        }
        
        response = self.make_request('POST', '/auth/token/', login_data, auth_required=False)
        
        if response['success']:
            self.access_token = response['data'].get('access')
            self.refresh_token = response['data'].get('refresh')
        
        self.log_result(
            "User Login",
            response['success'],
            f"Status: {response['status_code']}, Got tokens: {bool(self.access_token)}"
        )
        
        return response['success']

    def test_get_user_profile(self):
        """Test getting current user profile"""
        print("\n🔍 Testing Get User Profile...")
        
        response = self.make_request('GET', '/auth/me/')
        
        if response['success']:
            self.user_id = response['data'].get('id')
        
        self.log_result(
            "Get User Profile",
            response['success'],
            f"Status: {response['status_code']}, User ID: {self.user_id}"
        )

    def test_update_user_profile(self):
        """Test updating user profile"""
        print("\n🔍 Testing Update User Profile...")
        
        update_data = {
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        response = self.make_request('PATCH', '/auth/me/', update_data)
        
        self.log_result(
            "Update User Profile",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_products_crud(self):
        """Test product CRUD operations"""
        print("\n🔍 Testing Product CRUD Operations...")
        
        # Test getting products list
        response = self.make_request('GET', '/products')
        self.log_result(
            "Get Products List",
            response['success'],
            f"Status: {response['status_code']}"
        )
        
        # Test creating a product
        product_data = {
            'name': 'Test Maize',
            'category': 'GRAINS',
            'description': 'High quality test maize',
            'quantity': 100.0,
            'unit': 'kg',
            'price_per_unit': 350.0,
            'harvest_date': '2024-12-01',
            'location': 'Lilongwe',
            'contact_phone': '+265999123456'
        }
        
        response = self.make_request('POST', '/products', product_data)
        product_id = None
        if response['success']:
            product_id = response['data'].get('id')
        
        self.log_result(
            "Create Product",
            response['success'],
            f"Status: {response['status_code']}, Product ID: {product_id}"
        )
        
        # Test updating the product
        if product_id:
            update_data = {
                'name': 'Updated Test Maize',
                'description': 'Updated description'
            }
            response = self.make_request('PATCH', f'/products/{product_id}', update_data)
            self.log_result(
                "Update Product",
                response['success'],
                f"Status: {response['status_code']}"
            )
            
            # Test getting specific product
            response = self.make_request('GET', f'/products/{product_id}')
            self.log_result(
                "Get Specific Product",
                response['success'],
                f"Status: {response['status_code']}"
            )
            
            # Test deleting the product
            response = self.make_request('DELETE', f'/products/{product_id}')
            self.log_result(
                "Delete Product",
                response['success'],
                f"Status: {response['status_code']}"
            )

    def test_community_crud(self):
        """Test community forum CRUD operations"""
        print("\n🔍 Testing Community Forum Operations...")
        
        # Test getting posts list
        response = self.make_request('GET', '/community/posts')
        self.log_result(
            "Get Community Posts",
            response['success'],
            f"Status: {response['status_code']}"
        )
        
        # Test creating a post
        post_data = {
            'title': 'Test Question about Maize',
            'content': 'I need help with my maize crop. What fertilizer should I use?',
            'category': 'question',
            'is_question': True
        }
        
        response = self.make_request('POST', '/community/posts', post_data)
        post_id = None
        if response['success']:
            post_id = response['data'].get('id')
        
        self.log_result(
            "Create Community Post",
            response['success'],
            f"Status: {response['status_code']}, Post ID: {post_id}"
        )
        
        # Test adding a reply
        if post_id:
            reply_data = {
                'content': 'You should use NPK fertilizer for maize.'
            }
            response = self.make_request('POST', f'/community/posts/{post_id}/replies', reply_data)
            self.log_result(
                "Add Reply to Post",
                response['success'],
                f"Status: {response['status_code']}"
            )
            
            # Test liking the post
            response = self.make_request('POST', f'/community/posts/{post_id}/like')
            self.log_result(
                "Like Post",
                response['success'],
                f"Status: {response['status_code']}"
            )

    def test_market_prices(self):
        """Test market prices endpoints"""
        print("\n🔍 Testing Market Prices...")
        
        # Test getting market prices
        response = self.make_request('GET', '/market-prices')
        self.log_result(
            "Get Market Prices",
            response['success'],
            f"Status: {response['status_code']}"
        )
        
        # Test creating market price entry
        price_data = {
            'product_category': 'GRAINS',
            'market_name': 'Lilongwe Market',
            'location': 'Lilongwe',
            'price_per_unit': 400.0,
            'unit': 'kg',
            'currency': 'MWK',
            'source': 'Test Source'
        }
        
        response = self.make_request('POST', '/market-prices/create', price_data)
        self.log_result(
            "Create Market Price",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_weather_data(self):
        """Test weather data endpoint"""
        print("\n🔍 Testing Weather Data...")
        
        response = self.make_request('GET', '/weather')
        self.log_result(
            "Get Weather Data",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_newsletters(self):
        """Test newsletters endpoint"""
        print("\n🔍 Testing Newsletters...")
        
        response = self.make_request('GET', '/newsletters')
        self.log_result(
            "Get Newsletters",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_pest_diagnosis(self):
        """Test pest diagnosis endpoint"""
        print("\n🔍 Testing Pest Diagnosis...")
        
        # Test synchronous diagnosis
        diagnosis_data = {
            'crop_type': 'maize',
            'symptoms': 'Yellow leaves with brown spots'
        }
        
        response = self.make_request('POST', '/pest-diagnosis', diagnosis_data)
        self.log_result(
            "Pest Diagnosis (Sync)",
            response['success'],
            f"Status: {response['status_code']}"
        )
        
        # Test getting diagnosis history
        response = self.make_request('GET', '/pest-diagnosis')
        self.log_result(
            "Get Diagnosis History",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def test_token_refresh(self):
        """Test JWT token refresh"""
        print("\n🔍 Testing Token Refresh...")
        
        if not self.refresh_token:
            self.log_result("Token Refresh", False, "No refresh token available")
            return
        
        refresh_data = {
            'refresh': self.refresh_token
        }
        
        response = self.make_request('POST', '/auth/token/refresh/', refresh_data, auth_required=False)
        
        if response['success']:
            self.access_token = response['data'].get('access')
        
        self.log_result(
            "Token Refresh",
            response['success'],
            f"Status: {response['status_code']}"
        )

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Mlimi API Tests...")
        print(f"Testing against: {self.base_url}")
        
        # Test health check first
        self.test_health_check()
        
        # Test user registration and login
        user_data = self.test_user_registration()
        if user_data:
            login_success = self.test_user_login(user_data['username'], user_data['password'])
            
            if login_success:
                # Test authenticated endpoints
                self.test_get_user_profile()
                self.test_update_user_profile()
                self.test_products_crud()
                self.test_community_crud()
                self.test_market_prices()
                self.test_weather_data()
                self.test_newsletters()
                self.test_pest_diagnosis()
                self.test_token_refresh()
            else:
                print("❌ Skipping authenticated tests due to login failure")
        else:
            print("❌ Skipping all tests due to registration failure")
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"🎯 Success Rate: {self.test_results['passed']/(self.test_results['passed']+self.test_results['failed'])*100:.1f}%")
        
        if self.test_results['errors']:
            print("\n💥 FAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        print("\n🏁 Testing Complete!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Mlimi Django API')
    parser.add_argument('--url', default='http://localhost:8000', 
                      help='Base URL of the Django server (default: http://localhost:8000)')
    
    args = parser.parse_args()
    
    tester = MlimiAPITester(args.url)
    tester.run_all_tests()

if __name__ == '__main__':
    main()