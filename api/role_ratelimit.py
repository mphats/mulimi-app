
from django.core.cache import cache
from django.http import JsonResponse
from functools import wraps
import time

ROLE_LIMITS = {
    'ADMIN': (120, 60),   # 120 requests per 60 seconds
    'AGRONOMIST': (60, 60),
    'TRADER': (40, 60),
    'FARMER': (30, 60),
    'ANONYMOUS': (10, 60)
}

def role_rate_limit(calls, period):
    """
    Decorator that applies rate limiting based on user role.
    Usage: @role_rate_limit(20, 60)  # 20 requests per 60 seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = getattr(request, 'user', None)
            role = getattr(getattr(user, 'profile', None), 'role', 'ANONYMOUS') if user and user.is_authenticated else 'ANONYMOUS'
            
            # Use the provided rate limit or fall back to role-based limits
            role_calls, role_period = ROLE_LIMITS.get(role, ROLE_LIMITS['ANONYMOUS'])
            actual_calls = min(calls, role_calls)  # Use the more restrictive limit
            actual_period = max(period, role_period)  # Use the longer period
            
            key = f"rate:{role}:{request.path}:{getattr(user,'id','anon')}"
            now = int(time.time())
            window = now // actual_period
            cache_key = f"{key}:{window}"
            count = cache.get(cache_key, 0)
            
            if count >= actual_calls:
                return JsonResponse({'detail': 'rate limit exceeded'}, status=429)
            
            cache.set(cache_key, count+1, timeout=actual_period)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
