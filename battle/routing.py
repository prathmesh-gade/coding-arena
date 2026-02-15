from django.urls import re_path
from .consumers import BattleConsumer

websocket_urlpatterns = [
    re_path(
        r"^ws/battle/(?P<room>\w+)/$",
        BattleConsumer.as_asgi()
    ),
]
