import os
import django
from pathlib import Path

# Add project to Python path
project_dir = Path(__file__).resolve().parent
os.chdir(project_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_sqlite')

def main():
    try:
        django.setup()
        print("✅ Django setup successful")
        
        # Create a test user
        from django.contrib.auth.models import User
        
        # Check if user already exists
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='2000Fh22@'
            )
            print(f"✅ Created superuser: {user.username}")
        else:
            print("✅ Superuser 'admin' already exists")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()