import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_api_trade_list():
    client = APIClient()
    response = client.get(reverse("trade-list"))
    assert response.status_code == 200
