import asyncio
import json

import websockets
from channels.generic.websocket import AsyncWebsocketConsumer


class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]
        await self.accept()

        await self.send(json.dumps({"message": "WebSocket is working"}))

        self.binance_task = asyncio.create_task(self.listen_to_binance())

    async def disconnect(self, close_code):
        if hasattr(self, "binance_task"):
            self.binance_task.cancel()

    async def receive(self, text_data):
        pass

    async def listen_to_binance(self):
        binance_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        print(f"Connected to Binance: {binance_url}")

        try:
            async with websockets.connect(binance_url) as ws:
                while True:
                    data = await ws.recv()
                    trade_data = json.loads(data)
                    trade = {
                        "symbol": trade_data["s"],
                        "price": trade_data["p"],
                        "timestamp": trade_data["T"],
                    }
                    print(f"A new deal ({self.symbol.upper()}): {trade}")
                    await self.send(json.dumps(trade))
        except Exception as e:
            print(f"WebSocket Binance error: {e}")
