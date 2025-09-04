#!/usr/bin/env python3
"""
Android Emulator Connectivity Test
This script helps diagnose connectivity issues between Android emulator and Django server.
"""

import socket
import subprocess
import requests
import time
import json

def test_port_accessibility():
    """Test if port 8000 is accessible on different interfaces."""
    print("Testing Port 8000 Accessibility:")
    print("-" * 40)
    
    interfaces = [
        ("127.0.0.1", "Localhost"),
        ("0.0.0.0", "All interfaces"),
    ]
    
    for host, description in interfaces:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                result = s.connect_ex((host, 8000))
                status = "✓ ACCESSIBLE" if result == 0 else "✗ NOT ACCESSIBLE"
                print(f"{description:20} ({host}:8000): {status}")
        except Exception as e:
            print(f"{description:20} ({host}:8000): ✗ ERROR - {e}")
    print()

def test_django_health_endpoint():
    """Test Django health endpoint on different URLs."""
    print("Testing Django Health Endpoint:")
    print("-" * 40)
    
    urls = [
        "http://127.0.0.1:8000/api/v1/health",
        "http://localhost:8000/api/v1/health",
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ {url}: {response.status_code} - {response.json().get('status', 'OK')}")
            else:
                print(f"✗ {url}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ {url}: ERROR - {e}")
    print()

def check_windows_firewall():
    """Check Windows Firewall status for port 8000."""
    print("Checking Windows Firewall:")
    print("-" * 40)
    
    try:
        # Check firewall rules for port 8000
        result = subprocess.run([
            "netsh", "advfirewall", "firewall", "show", "rule", 
            "name=all", "dir=in", "protocol=tcp", "localport=8000"
        ], capture_output=True, text=True)
        
        if "No rules match the specified criteria" in result.stdout:
            print("✗ No firewall rules found for port 8000")
            print("  Run 'configure_firewall.bat' as Administrator to fix this")
        else:
            print("✓ Firewall rules found for port 8000")
            print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
    except Exception as e:
        print(f"✗ Could not check firewall: {e}")
    print()

def get_network_info():
    """Get network interface information."""
    print("Network Interface Information:")
    print("-" * 40)
    
    try:
        # Get IPv4 addresses
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for i, line in enumerate(lines):
            if "IPv4 Address" in line:
                ip = line.split(':')[-1].strip()
                adapter_name = ""
                # Look backwards for adapter name
                for j in range(i-1, max(i-10, 0), -1):
                    if "adapter" in lines[j].lower():
                        adapter_name = lines[j].strip()
                        break
                
                print(f"Interface: {adapter_name}")
                print(f"IPv4: {ip}")
                print()
    except Exception as e:
        print(f"✗ Could not get network info: {e}")
    print()

def provide_solutions():
    """Provide step-by-step solutions."""
    print("SOLUTIONS TO TRY:")
    print("=" * 50)
    
    print("1. FIREWALL CONFIGURATION (Most likely fix):")
    print("   - Open Command Prompt as Administrator")
    print("   - Run: configure_firewall.bat")
    print("   - Or manually: netsh advfirewall firewall add rule name=\"Django\" dir=in action=allow protocol=TCP localport=8000")
    print()
    
    print("2. RESTART DJANGO SERVER:")
    print("   - Stop current server (Ctrl+C)")
    print("   - Run: python manage.py runserver 0.0.0.0:8000")
    print("   - Ensure it shows 'Starting development server at http://0.0.0.0:8000/'")
    print()
    
    print("3. ANDROID EMULATOR NETWORK:")
    print("   - In Android emulator, use: http://10.0.2.2:8000/api/v1")
    print("   - NOT http://127.0.0.1:8000 or http://localhost:8000")
    print("   - 10.0.2.2 is the special IP for host machine from Android emulator")
    print()
    
    print("4. TEST CONNECTIVITY:")
    print("   - From Windows: curl http://127.0.0.1:8000/api/v1/health")
    print("   - Should return: {\"status\": \"healthy\"}")
    print()
    
    print("5. WINDOWS DEFENDER/ANTIVIRUS:")
    print("   - Check if Windows Defender is blocking Python.exe")
    print("   - Add Python.exe to firewall exceptions")
    print("   - Temporarily disable real-time protection for testing")
    print()

def main():
    """Main diagnostic function."""
    print("ANDROID EMULATOR CONNECTIVITY DIAGNOSTIC")
    print("=" * 50)
    print()
    
    test_port_accessibility()
    test_django_health_endpoint()
    check_windows_firewall()
    get_network_info()
    provide_solutions()

if __name__ == "__main__":
    main()