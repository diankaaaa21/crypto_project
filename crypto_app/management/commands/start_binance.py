import asyncio

from django.core.management.base import BaseCommand

from crypto_app.binance_ws import start_binance


class Command(BaseCommand):
    help = "Connect WebSocket client Binance"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Connecting Binance WebSocket..."))
        asyncio.run(start_binance())
