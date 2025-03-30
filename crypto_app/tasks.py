from datetime import datetime

from celery import shared_task

from .models import Trade


@shared_task
def save_trade(symbol, price, quantity, trade_time):

    trade = Trade(
        symbol=symbol,
        price=float(price),
        quantity=float(quantity),
        trade_time=datetime.fromtimestamp(trade_time / 1000),
    )
    trade.save()


@shared_task
def start_binance():
    import asyncio
<<<<<<< HEAD

    from .binance_ws import fetch_trades

    symbols = ["btcusdt", "ethusdt", "bnbusdt"]
    loop = asyncio.get_event_loop()
    for symbol in symbols:
        loop.create_task(fetch_trades(symbol))
=======
>>>>>>> b632589 (initial)

    from .binance_ws import fetch_trades

    symbols = ["btcusdt", "ethusdt", "bnbusdt"]
    loop = asyncio.get_event_loop()
    for symbol in symbols:
        loop.create_task(fetch_trades(symbol))
