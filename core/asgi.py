
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import ai.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ai.routing.websocket_urlpatterns
        )
    ),
})
