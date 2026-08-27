import asyncio
import json
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from crypto_project.shortcuts import file_logger

logger = file_logger('crypto_app_ws')


class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"].lower()
        await self.accept()
        logger.info(f"WebSocket connected for: {self.symbol}")

        await self.send(text_data=json.dumps({"message": f"Connected to {self.symbol.upper()}"}))

        self.binance_task = asyncio.create_task(self.listen_to_binance())

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting WebSocket for: {self.symbol}")
        if hasattr(self, "binance_task") and not self.binance_task.done():
            self.binance_task.cancel()
            try:
                await self.binance_task
            except asyncio.CancelledError:
                logger.info(f"Binance stream task cancelled for {self.symbol}")

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def listen_to_binance(self):
        url = f"wss://stream.binance.com:9443/ws/{self.symbol}@trade"
        logger.info(f"Connecting to Binance: {url}")
        try:
            async with websockets.connect(url) as ws:
                while True:
                    message = await ws.recv()
                    trade_data = json.loads(message)
                    trade = {
                        "symbol": trade_data.get("s"),
                        "price": trade_data.get("p"),
                        "timestamp": trade_data.get("T"),
                    }
                    await self.send(text_data=json.dumps(trade))
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Binance WebSocket error for {self.symbol}: {e}")
            try:
                await self.send(text_data=json.dumps({"message": f"Error: {str(e)}"}))
            except Exception:
                pass