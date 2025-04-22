import pytest
from channels.testing import WebsocketCommunicator

from crypto_project.asgi import application


@pytest.mark.asyncio
async def test_only_websocket_connect_message():
    communicator = WebsocketCommunicator(application, "/ws/trades/btcusdt/")
    connected, _ = await communicator.connect()
    assert connected

    response = await communicator.receive_json_from(timeout=2)
    assert response == {"message": "WebSocket connected"}

    await communicator.disconnect()
