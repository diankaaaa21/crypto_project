"""
ASGI config for crypto_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import asyncio
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from crypto_app.routing import websocket_urlpatterns

# from crypto_app.consumer_logic import start_sending
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)

# async def start_sending_loop():
#     import asyncio
#     from crypto_app.consumer_logic import start_sending  # Импортируй свою функцию здесь
#     loop = asyncio.get_event_loop()
#     loop.create_task(start_sending())
#
# # Запускаем фоновую задачу после загрузки ASGI-приложения
# import threading
# threading.Thread(target=lambda: asyncio.run(start_sending_loop()), daemon=True).start()
