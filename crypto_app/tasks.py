import asyncio
from datetime import datetime

from celery import shared_task
from twisted.plugins.twisted_reactors import asyncio

from .binance_ws import start_binance
from .models import Trade


@shared_task(name="crypto_app.tasks.save_trade")
def save_trade(symbol, price, quantity, trade_time):

    trade = Trade(
        symbol=symbol,
        price=float(price),
        quantity=float(quantity),
        trade_time=datetime.fromtimestamp(trade_time / 1000),
    )
    trade.save()
