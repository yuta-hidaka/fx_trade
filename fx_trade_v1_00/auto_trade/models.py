from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class batchLog(models.Model):
    text = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

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
    m5 = models.ForeignKey(
        'M5_USD_JPY', on_delete=models.CASCADE, related_name='m5', null=True)
    m5_ma5 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma6 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma10 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma12 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma15 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma20 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma24 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma30 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma36 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma40 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma50 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma70 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma72 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma75 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma140 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma144 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma150 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    m5_ma288 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'MA_USD_JPY'


# 平均移動線の傾き
# プラスであれば傾きが大きくなっており、マイナスは縮小
class SlopeM5_USD_JPY(models.Model):
    ma_previous = models.ForeignKey(
        'MA_USD_JPY', on_delete=models.CASCADE, related_name='ma_previous', null=True)

    ma_leatest = models.ForeignKey(
        'MA_USD_JPY', on_delete=models.CASCADE, related_name='ma_leatest', null=True)

    slope_m5_ma5 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma6 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma10 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma12 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma15 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma20 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma24 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma30 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma36 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma40 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma50 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma70 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma72 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma75 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma140 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma144 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma150 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    slope_m5_ma288 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slope_MA_M5_USD_JPY'


# 短期、中期、長期の状態


class listConditionOfMA(models.Model):
    condition = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'list_condition_of_ma'

# 傾きの状態

# すべて傾きが正、すべて傾きが負、それ以外


class listConditionOfSlope(models.Model):
    condition = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'list_condition_of_slope'


# BBから計算したBBバンドのトレンドを考える
class listConditionOfBBTrande(models.Model):
    condition = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'list_condition_of_BB_trande'


# # BBから計算したBBバンドのトレンドを考える
# class listConditionOfBBTrande(models.Model):
#     condition = models.CharField(max_length=256)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'list_condition_of_BB_trande'


# ボリンジャーバンドの状態からconditionを検証。(トレンド判定とレンジ相場中での売買判定)
class conditionOfBB(models.Model):
    is_expansion = models.BooleanField(null=True, default=False)
    is_topTouch = models.BooleanField(null=True, default=False)
    is_bottomTouch = models.BooleanField(null=True, default=False)
    is_shortIn = models.BooleanField(null=True)
    is_expansionByStd = models.BooleanField(null=True)
    bb_trande = models.ForeignKey(
        'listConditionOfBBTrande', on_delete=models.CASCADE, related_name='bb_trande', null=True)
    bb = models.ForeignKey(
        'bollingerBand', on_delete=models.CASCADE, related_name='bb', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condition_of_bb'

# ボリンジャーバンドの値計算


class bollingerBand(models.Model):
    sma_M50 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000, null=True)
    abs_sigma_1 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000, null=True)
    abs_sigma_2 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000, null=True)
    abs_sigma_3 = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000, null=True)
    recorded_at_utc = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bollinger_band'


class conditionOfSlope_M5(models.Model):
    slope_comp1_6_24 = models.ForeignKey(
        'listConditionOfSlope', on_delete=models.CASCADE, related_name='slope_comp1_6_24', null=True)

    slope_comp5_20_75 = models.ForeignKey(
        'listConditionOfSlope', on_delete=models.CASCADE, related_name='slope_comp5_20_75', null=True)

    slope_comp5_20_40 = models.ForeignKey(
        'listConditionOfSlope', on_delete=models.CASCADE, related_name='slope_comp5_20_40', null=True)

    slope_comp6_24_72 = models.ForeignKey(
        'listConditionOfSlope', on_delete=models.CASCADE, related_name='slope_comp6_24_72', null=True)

    slope_comp6_24_50 = models.ForeignKey(
        'listConditionOfSlope', on_delete=models.CASCADE, related_name='slope_comp6_24_50', null=True)

    ma = models.ForeignKey(
        'MA_USD_JPY', on_delete=models.CASCADE, related_name='ma_slope')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condition_of_slope'


class conditionOfMA_M5(models.Model):
    ma_comp1_6_24 = models.ForeignKey(
        'listConditionOfMA', on_delete=models.CASCADE, related_name='ma_comp1_6_24', null=True)

    ma_comp6_24_72 = models.ForeignKey(
        'listConditionOfMA', on_delete=models.CASCADE, related_name='ma_comp6_24_72', null=True)

    ma_comp5_20_40 = models.ForeignKey(
        'listConditionOfMA', on_delete=models.CASCADE, related_name='ma_comp5_20_40', null=True)

    ma_comp5_20_75 = models.ForeignKey(
        'listConditionOfMA', on_delete=models.CASCADE, related_name='ma_comp5_20_75', null=True)

    ma_comp6_24_50 = models.ForeignKey(
        'listConditionOfMA', on_delete=models.CASCADE, related_name='ma_comp6_24_50', null=True)

    ma = models.ForeignKey(
        'MA_USD_JPY', on_delete=models.CASCADE, related_name='ma')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condition_of_ma'


# maを中心とした現状を示す指標の集合体。


class condition(models.Model):
    ma = models.ForeignKey(
        'MA_USD_JPY', on_delete=models.CASCADE, related_name='condition_ma', null=True)
    condition_of_slope_M5 = models.ForeignKey(
        'conditionOfSlope_M5', on_delete=models.CASCADE, related_name='conditionOfSlope_M5', null=True)
    condition_of_ma_M5 = models.ForeignKey(
        'conditionOfMA_M5', on_delete=models.CASCADE, related_name='conditionOfSlope_M5', null=True)
    condition_of_bb = models.ForeignKey(
        'conditionOfBB', on_delete=models.CASCADE, related_name='condition_of_bb', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'condition'

# 自動取引のON,OFFを決める


class sellBuyAlert(models.Model):
    position_in = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    position_out = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    position_def = models.DecimalField(
        max_digits=8, decimal_places=4, default=0.0000)
    is_buy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sell_buy_alert'

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


# バッチの起動時間を記録するモデル
class orderStatus(models.Model):
    short_order = models.IntegerField(default=0)
    long_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_status'
