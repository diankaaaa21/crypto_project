from django.db import models


class Trade(models.Model):
    trade_id = models.BigIntegerField(unique=True, null=True, blank=True)
    symbol = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    trade_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["symbol", "trade_id"],
                name="unique_symbol_trade"
            )
        ]
