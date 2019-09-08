from django.db import models

# Create your models here.


class autoTradeOnOff(models.Model):
    auto_trade_is_on = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auto_trade_on_off'
