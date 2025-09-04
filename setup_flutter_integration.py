#!/usr/bin/env python3
"""
Flutter-Django Integration Setup Script
This script sets up the complete Flutter mobile app with Django backend integration.
"""

import os
import sys
import subprocess
import json

def run_command(command, cwd=None, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python
    success, stdout, stderr = run_command("python --version")
    if success:
        print(f"✅ Python: {stdout.strip()}")
    else:
        print("❌ Python not found")
        return False
    
    # Check Flutter
    success, stdout, stderr = run_command("flutter --version")
    if success:
        flutter_version = stdout.split('\n')[0]
        print(f"✅ Flutter: {flutter_version}")
    else:
        print("❌ Flutter not found")
        return False
    
    # Check Django
    success, stdout, stderr = run_command("python -c \"import django; print(f'Django {django.get_version()}')\"")
    if success:
        print(f"✅ {stdout.strip()}")
    else:
        print("❌ Django not found")
        return False
    
    return True

def setup_django_backend():
    """Setup Django backend"""
    print("\n🚀 Setting up Django backend...")
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements.txt")
    if not success:
        print(f"❌ Failed to install Python dependencies: {stderr}")
        return False
    print("✅ Python dependencies installed")
    
    # Run migrations
    print("🗄️ Running database migrations...")
    success, stdout, stderr = run_command("python manage.py migrate")
    if not success:
        print(f"❌ Failed to run migrations: {stderr}")
        return False
    print("✅ Database migrations completed")
    
    # Create superuser (optional)
    print("👤 Creating superuser (optional)...")
    success, stdout, stderr = run_command("python manage.py createsuperuser --noinput", capture_output=False)
    
    # Collect static files
    print("📁 Collecting static files...")
    success, stdout, stderr = run_command("python manage.py collectstatic --noinput")
    if success:
        print("✅ Static files collected")
    
    return True

def setup_flutter_app():
    """Setup Flutter mobile app"""
    print("\n📱 Setting up Flutter mobile app...")
    
    flutter_dir = "flutter_mobile_app/mulimi"
    
    if not os.path.exists(flutter_dir):
        print(f"❌ Flutter directory not found: {flutter_dir}")
        return False
    
    # Get Flutter dependencies
    print("📦 Installing Flutter dependencies...")
    success, stdout, stderr = run_command("flutter pub get", cwd=flutter_dir)
    if not success:
        print(f"❌ Failed to install Flutter dependencies: {stderr}")
        return False
    print("✅ Flutter dependencies installed")
    
    # Check Flutter app
    print("🔍 Analyzing Flutter app...")
    success, stdout, stderr = run_command("flutter analyze", cwd=flutter_dir)
    if success:
        print("✅ Flutter app analysis passed")
    else:
        print(f"⚠️ Flutter analysis warnings: {stderr}")
    
    return True

def create_configuration_files():
    """Create necessary configuration files"""
    print("\n⚙️ Creating configuration files...")
    
    # Create Flutter launch configuration
    flutter_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Mlimi (Debug)",
                "request": "launch",
                "type": "dart",
                "cwd": "flutter_mobile_app/mulimi",
                "args": ["--flavor", "development"]
            },
            {
                "name": "Mlimi (Release)",
                "request": "launch",
                "type": "dart",
                "cwd": "flutter_mobile_app/mulimi",
                "flutterMode": "release"
            }
        ]
    }
    
    os.makedirs(".vscode", exist_ok=True)
    with open(".vscode/launch.json", "w") as f:
        json.dump(flutter_config, f, indent=2)
    
    print("✅ Configuration files created")

def test_integration():
    """Test Django-Flutter integration"""
    print("\n🧪 Testing Django-Flutter integration...")
    
    # Test Django health check
    success, stdout, stderr = run_command("python test_flutter_integration.py --url http://localhost:8000")
    if success:
        print("✅ Django API tests passed")
    else:
        print(f"❌ Django API tests failed: {stderr}")
    
    return success

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Start the Django development server:")
    print("   python manage.py runserver")
    print("\n2. In a new terminal, start the Flutter app:")
    print("   cd flutter_mobile_app/mulimi")
    print("   flutter run")
    print("\n3. For Android emulator:")
    print("   - Make sure an Android emulator is running")
    print("   - Or connect a physical Android device")
    print("\n4. API Base URL Configuration:")
    print("   - Android Emulator: http://10.0.2.2:8000")
    print("   - iOS Simulator: http://localhost:8000")
    print("   - Physical Device: http://YOUR_COMPUTER_IP:8000")
    print("\n5. Test the integration:")
    print("   - Register a new user in the Flutter app")
    print("   - Try logging in")
    print("   - Explore the dashboard features")
    print("\n🔧 Troubleshooting:")
    print("   - Check Django admin at: http://localhost:8000/admin/")
    print("   - API documentation at: http://localhost:8000/api/schema/swagger-ui/")
    print("   - Flutter app logs: flutter logs")

def main():
    """Main setup function"""
    print("🚀 Mlimi Flutter-Django Integration Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Setup Django backend
    if not setup_django_backend():
        print("\n❌ Django backend setup failed.")
        sys.exit(1)
    
    # Setup Flutter app
    if not setup_flutter_app():
        print("\n❌ Flutter app setup failed.")
        sys.exit(1)
    
    # Create configuration files
    create_configuration_files()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()