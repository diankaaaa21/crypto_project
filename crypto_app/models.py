from django.db import models


class Trade(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    trade_time = models.DateTimeField()

    objects = models.Manager()
