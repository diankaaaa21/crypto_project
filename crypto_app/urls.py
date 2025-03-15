from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import trade_html_view

urlpatterns = [
    re_path("trades/", trade_html_view, name="trade_html"),
]
