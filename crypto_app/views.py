from rest_framework import viewsets

from .models import Trade
from .serializers import TradeSerializer


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all().order_by("-trade_time")
    serializer_class = TradeSerializer

    def get_queryset(self):

        symbol = self.request.query_params.get("symbol")
        queryset = Trade.objects.all().order_by("-trade_time")

        if symbol:
            queryset = queryset.filter(symbol=symbol.upper())

        return queryset
