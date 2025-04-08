from django.urls import path, re_path

from .views import trade_html_view

urlpatterns = [
    re_path("trades/", trade_html_view, name="trade_html"),
]
