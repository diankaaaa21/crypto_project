from unittest.mock import patch

import pytest

from crypto_app.binance_ws import fetch_trades


@patch("crypto_app.binance_ws.websockets")
def test_binance_data(mock_ws_app):
    mock_instance = mock_ws_app.return_value
    mock_instance.run_forever.return_value = None

    result = fetch_trades("btcusdt")
    assert result is not None
