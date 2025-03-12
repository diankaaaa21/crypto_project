import asyncio
import websockets

async def test_binance():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    try:
        print("Connecting to Binance WebSocket...")
        async with websockets.connect(url) as ws:
            while True:
                message = await ws.recv()
                print("Binance data:", message)
    except Exception as e:
        print(f"Connection error: {e}")

asyncio.run(test_binance())