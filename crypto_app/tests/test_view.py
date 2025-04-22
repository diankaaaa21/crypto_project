from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class TradeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            phone_number="testnum", first_name="testname", password="testpassword"
        )
        self.client.login(phone_number="testnum", password="testpassword")

    def test_trade_view(self):
        url = reverse("trade_html")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
