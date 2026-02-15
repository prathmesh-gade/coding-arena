import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

import battle.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codingarena.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    "websocket": AuthMiddlewareStack(
        URLRouter(
            battle.routing.websocket_urlpatterns
        )
    ),
})
