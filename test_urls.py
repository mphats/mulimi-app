import os
import django
from django.urls import resolve, reverse

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_sqlite')
django.setup()

try:
    # Test if the URL pattern exists
    url = reverse('users:token_obtain_pair')
    print(f"✅ URL pattern found: {url}")
except Exception as e:
    print(f"❌ Error resolving URL: {e}")
    
try:
    # Test with the full path
    from django.urls import get_resolver
    resolver = get_resolver()
    match = resolver.resolve('/api/v1/auth/token/')
    print(f"✅ URL resolved successfully: {match}")
except Exception as e:
    print(f"❌ Error resolving URL path: {e}")

# Print all URL patterns
print("\n🔍 All URL patterns:")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        print(f"  - {pattern.pattern}")
except Exception as e:
    print(f"❌ Error getting URL patterns: {e}")