import pytest
from django.utils import timezone

from crypto_app.models import Trade


@pytest.mark.django_db
def test_trade_creation():
    trade = Trade.objects.create(
        symbol="BTCUSDT", price="65000.00", quantity="0.05", trade_time=timezone.now()
    )

    assert trade.id is not None
    assert trade.symbol == "BTCUSDT"
    assert float(trade.price) == 65000.00
    assert float(trade.quantity) == 0.05

    assert Trade.objects.count() == 1
