import asyncio
import json
import logging

import websockets
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.symbol = self.scope["url_route"]["kwargs"]["symbol"]
        await self.accept()
        logger.info(f"WebSocket connected for: {self.symbol}")
        await self.send(text_data=json.dumps({"message": "WebSocket connected"}))

        self.binance_task = asyncio.create_task(self.listen_to_binance())

    async def disconnect(self, close_code):
        if hasattr(self, "binance_task"):
            self.binance_task.cancel()
            try:
                await self.binance_task
            except asyncio.CancelledError:
                logger.info("Binance stream cancelled")

    async def receive(self, text_data):
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
                    logger.info(f"New trade: {trade}")
                    await self.send(text_data=json.dumps(trade))
        except Exception as e:
            logger.error(f"Binance WebSocket error: {e}")
            await self.send(text_data=json.dumps({"message": f"Error: {str(e)}"}))
