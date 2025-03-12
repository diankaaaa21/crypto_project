import pytest
import asyncio
import websockets


async def mock_django_ws(websocket, path):
    await websocket.send("Hello, WebSocket!")


@pytest.fixture
async def websocket_server():
    server = await websockets.serve(mock_django_ws, "127.0.0.1", 8000)


    await asyncio.sleep(0.1)

    yield server


    server.close()
    await server.wait_closed()


@pytest.mark.asyncio
async def test_websocket_server(websocket_server):
    async with websockets.connect("ws://127.0.0.1:8000") as ws:
        message = await ws.recv()
        assert message == "Hello, WebSocket!"

