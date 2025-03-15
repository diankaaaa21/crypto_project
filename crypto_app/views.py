from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Trade


def get_queryset(self):
    symbol = self.request.query_params.get("symbol")
    queryset = Trade.objects.all().order_by("-trade_time")

    if symbol:
        queryset = queryset.filter(symbol=symbol.upper())

    return queryset


def trade_html_view(request):
    symbol = request.GET.get("symbol")
    trades = Trade.objects.all().order_by("-trade_time")

    if symbol:
        trades = trades.filter(symbol=symbol.upper())

    paginator = Paginator(trades, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "crypto_app/crypto_view.html",
        {"trades": page_obj, "selected_symbol": symbol},
    )
