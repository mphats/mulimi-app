"""
Quick test script to verify Django server is reachable from Flutter emulator
"""

import requests
import sys

def test_urls():
    urls = [
        'http://127.0.0.1:8000/api/v1/health',  # Localhost
        'http://10.0.2.2:8000/api/v1/health',  # Android emulator URL (won't work from Windows)
        'http://0.0.0.0:8000/api/v1/health',   # All interfaces (may not work)
    ]
    
    print("Testing Django server connectivity...\n")
    
    for url in urls:
        print(f"Testing: {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ SUCCESS - Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except requests.exceptions.ConnectionError:
            print("❌ CONNECTION ERROR - Server not reachable")
        except requests.exceptions.Timeout:
            print("❌ TIMEOUT - Server too slow to respond")
        except Exception as e:
            print(f"❌ ERROR - {e}")
        print()

if __name__ == '__main__':
    test_urls()