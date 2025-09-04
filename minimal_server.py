import os
import sys
from pathlib import Path

# Add project to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_sqlite')

def main():
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Setup Django
        django.setup()
        
        print("✅ Django setup successful")
        
        # Try to import the URL configuration
        from django.urls import get_resolver
        resolver = get_resolver()
        
        print("✅ URL resolver loaded")
        
        # Check if our specific URL exists
        try:
            from django.urls import reverse
            url = reverse('users:token_obtain_pair')
            print(f"✅ Token URL found: {url}")
        except Exception as e:
            print(f"❌ Error finding token URL: {e}")
            
        # List some URL patterns
        print("\n📋 Sample URL patterns:")
        count = 0
        for pattern in resolver.url_patterns:
            if count < 10:  # Only show first 10
                print(f"  - {pattern.pattern}")
                count += 1
            else:
                print("  ... (more patterns)")
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()