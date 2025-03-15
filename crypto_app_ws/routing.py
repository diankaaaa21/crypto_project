from django.urls import re_path

from crypto_app_ws.consumers import TradeConsumer

websocket_urlpatterns = [
    re_path(r"ws/trades/(?P<symbol>\w+)/$", TradeConsumer.as_asgi()),
]
