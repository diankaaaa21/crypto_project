from django.core.cache import cache
from django.core.paginator import Paginator

from crypto_app.models import Trade


def get_paginator_trade(
    symbol: str, page_number: str, per_page: int = 50, timeout: int = 60
):
    cache_key = f"trade_{symbol}_page_{page_number}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    trades = Trade.objects.only(
        "symbol", "price", "trade_time").order_by("-trade_time")

    if symbol:
        trades = trades.filter(symbol=symbol.upper())

    paginator = Paginator(trades, 50)
    page = paginator.get_page(page_number)
    serialized = list(page.object_list.values("symbol", "price", "trade_time"))
    page_data = {
        "data": serialized,
        "number": page.number,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "num_pages": paginator.num_pages,
    }

    cache.set(cache_key, page_data, timeout=60)

    return page_data
