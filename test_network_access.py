#!/usr/bin/env python3
"""
Network accessibility test for Django server.
This script tests if the Django server is accessible from different network interfaces.
"""

import socket
import requests
import time
from urllib.parse import urljoin

def test_port_open(host, port, timeout=3):
    """Test if a port is open on a given host."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

def test_http_endpoint(base_url, endpoint='/api/v1/health', timeout=3):
    """Test if an HTTP endpoint is accessible."""
    try:
        url = urljoin(base_url, endpoint)
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote server to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return None

def main():
    """Main test function."""
    print("Django Server Network Accessibility Test")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    print()
    
    # Test different host configurations
    test_hosts = [
        ("127.0.0.1", "Localhost"),
        ("0.0.0.0", "All interfaces"),
        (local_ip, "Local network IP") if local_ip else None,
    ]
    
    # Remove None entries
    test_hosts = [host for host in test_hosts if host is not None]
    
    port = 8000
    
    print("Testing Port Accessibility:")
    print("-" * 30)
    for host, description in test_hosts:
        is_open = test_port_open(host, port)
        status = "✓ OPEN" if is_open else "✗ CLOSED"
        print(f"{description:20} ({host}:{port}): {status}")
    
    print()
    print("Testing HTTP Endpoints:")
    print("-" * 30)
    
    # Test HTTP endpoints
    base_urls = [
        "http://127.0.0.1:8000",
        f"http://{local_ip}:8000" if local_ip else None,
    ]
    
    # Remove None entries
    base_urls = [url for url in base_urls if url is not None]
    
    for base_url in base_urls:
        success, result = test_http_endpoint(base_url)
        status = f"✓ {result}" if success else f"✗ {result}"
        print(f"{base_url:25}: {status}")
    
    print()
    print("Flutter App URLs to test:")
    print("-" * 30)
    flutter_urls = [
        "http://10.0.2.2:8000/api/v1 (Android Emulator)",
        "http://127.0.0.1:8000/api/v1 (iOS Simulator)",
        f"http://{local_ip}:8000/api/v1 (Physical Device)" if local_ip else None,
    ]
    
    # Remove None entries
    flutter_urls = [url for url in flutter_urls if url is not None]
    
    for url in flutter_urls:
        print(f"  {url}")
    
    print()
    print("Recommendations:")
    print("-" * 30)
    
    if test_port_open("127.0.0.1", port):
        print("✓ Django server is running and accessible on localhost")
        print("✓ Android emulator should use: http://10.0.2.2:8000/api/v1")
        print("✓ iOS simulator should use: http://127.0.0.1:8000/api/v1")
        if local_ip and test_port_open(local_ip, port):
            print(f"✓ Physical devices should use: http://{local_ip}:8000/api/v1")
        else:
            print("⚠ For physical devices, start Django with:")
            print(f"  python manage.py runserver 0.0.0.0:8000")
    else:
        print("✗ Django server is not accessible")
        print("  Please start with: python manage.py runserver 127.0.0.1:8000")

if __name__ == "__main__":
    main()