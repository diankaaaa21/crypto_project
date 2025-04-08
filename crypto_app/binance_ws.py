import asyncio
import json
import logging

import websockets
from celery import current_app


async def fetch_trades(symbol):
    url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

    while True:
        try:
            async with websockets.connect(url, ping_interval=30) as websocket:
                logging.info(f"Connected to {url}")

                while True:
                    data = await websocket.recv()
                    data = json.loads(data)

                    current_app.send_task(
                        "crypto_app.tasks.save_trade",
                        args=[data["s"], data["p"], data["q"], data["T"]],
                    )

                    logging.debug(f"The data is saved: {data}")

        except websockets.exceptions.ConnectionClosed:
            logging.warning(f"Connection with {symbol} interrupted. Restarting...")
            await asyncio.sleep(5)

        except Exception as e:
            logging.critical(
                f"Error while retrieving data from  {symbol}: {e}", exc_info=True
            )
            await asyncio.sleep(10)


async def start_binance():
    symbols = ["btcusdt", "ethusdt", "bnbusdt"]
    await asyncio.gather(*(fetch_trades(symbol) for symbol in symbols))
