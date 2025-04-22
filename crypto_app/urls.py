from django.urls import re_path

from .views import trade_html_view

app_name = "crypto_app"

urlpatterns = [
    re_path("trades/", trade_html_view, name="trade_html"),
]
