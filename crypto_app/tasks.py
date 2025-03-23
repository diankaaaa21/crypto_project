import asyncio
import json
import logging
from datetime import datetime

import websockets
from asgiref.sync import async_to_sync
from celery import shared_task

from .models import Trade

logging.basicConfig(
    filename="crypto.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@shared_task
def save_trade(symbol, price, quantity, trade_time):

    trade = Trade(
        symbol=symbol,
        price=float(price),
        quantity=float(quantity),
        trade_time=datetime.fromtimestamp(trade_time / 1000),
    )
    trade.save()


async def fetch_trades(symbol):
    url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

    while True:
        try:
            async with websockets.connect(url, ping_interval=30) as websocket:
                logging.info(f"Connected to {url}")

                while True:
                    data = await websocket.recv()
                    data = json.loads(data)

                    save_trade.delay(
                        symbol=data["s"],
                        price=data["p"],
                        quantity=data["q"],
                        trade_time=data["T"],
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


@shared_task
def start_binance():
    symbols = ["btcusdt", "ethusdt", "bnbusdt"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*(fetch_trades(symbol) for symbol in symbols)))

