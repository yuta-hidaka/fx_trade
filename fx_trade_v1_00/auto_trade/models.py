from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


# 5分足
class M5_USD_JPY(models.Model):
    open = models.DecimalField(max_digits=8, decimal_places=4, default=0.0000)
    high = models.DecimalField(max_digits=8, decimal_places=4, default=0.0000)
    low = models.DecimalField(max_digits=8, decimal_places=4, default=0.0000)
    close = models.DecimalField(max_digits=8, decimal_places=4, default=0.0000)

    recorded_at_utc = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'M5_USD_JPY'

# 平均移動線


class MA_USD_JPY(models.Model):
    m5_ma5 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma10 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma15 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma20 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma30 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma40 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma50 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma70 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma75 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma140 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma150 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma288 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MA_USD_JPY'

# 自動取引のON,OFFを決める


class autoTradeOnOff(models.Model):
    auto_trade_is_on = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auto_trade_on_off'


# バッチの起動時間を記録するモデル
class batchRecord(models.Model):
    text = models.CharField(max_length=256, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'batch_record'
