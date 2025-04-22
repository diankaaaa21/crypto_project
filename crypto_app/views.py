from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services.crypto_sevice import get_paginator_trade


@login_required(login_url="my_auth:login")
def trade_html_view(request):

    symbol = request.GET.get("symbol")
    page_number = request.GET.get("page", "1")

    page_data = get_paginator_trade(symbol, page_number)

    context = {
        "trades": page_data["data"],
        "page_info": {
            "number": page_data["number"],
            "has_next": page_data["has_next"],
            "has_previous": page_data["has_previous"],
            "num_pages": page_data["num_pages"],
        },
        "selected_symbol": symbol,
    }

    return render(request, "crypto_app/crypto_view.html", context)
