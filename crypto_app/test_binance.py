import asyncio

import websockets


async def test_django_ws():
    selected_crypto = "BTCUSDT"
    url = f"ws://127.0.0.1:8000/ws/trades/{selected_crypto}"
    try:
        print(f"Connecting to {url}...")
        async with websockets.connect(url) as ws:
            while True:
                message = await ws.recv()
                print("Data from  WebSocket:", message)
    except Exception as e:
        print(f"Connection error: {e}")


asyncio.run(test_django_ws())
