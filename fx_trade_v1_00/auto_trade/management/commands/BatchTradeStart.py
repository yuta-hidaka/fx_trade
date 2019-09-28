from ...models import batchRecord, autoTradeOnOff, condition
from datetime import datetime, timedelta, timezone

import datetime
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from ...service.set_candle_USD_JPY import setCandle_USD_JPY
from ...calculate.buy_sell_cal import BuySellCal
from ...service.set_MA_USD_JPY import setMA_USD_JPY
from ...service.set_bollinger_band import setBollingerBand_USD_JPY
from ...service.set_candle_USD_JPY import setCandle_USD_JPY


# BaseCommandを継承して作成


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'auto trade batch'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        JST = timezone(timedelta(hours=+9), 'JST')
        dt_now = datetime.datetime.now(JST)
        setCandle = setCandle_USD_JPY()
        bsCal = BuySellCal()

        # バッチの実行状況を保存する。
        qSetBatch = batchRecord.objects.filter(id=1).first()

        # 5分足の保存
        result, created = setCandle.setM5()

# '----------------デバッグ用-------------------------------'
        # bb = setBollingerBand_USD_JPY()
        # BBCondi = bb.setBB()
        # setMA = setMA_USD_JPY()
        # condiPrev = condition.objects.latest('created_at')
        # condiNow = setMA.setMA(result, BBCondi)
        # bsCal.BuySellCheck(condiNow, condiPrev)
# '----------------デバッグ用-------------------------------'

        # 5分足が作成されたらMAを作成する。
        if created:
            # ボリンジャーバンドの設定
            bb = setBollingerBand_USD_JPY()
            BBCondi = bb.setBB()
            setMA = setMA_USD_JPY()
            condiPrev = condition.objects.latest('created_at')
            condiNow = setMA.setMA(result, BBCondi)
            bsCal.BuySellCheck(condiNow, condiPrev)

            # conditionListをもとに売買ポイントを考える。

        # 自動取引がOFFかONかを確認する。
        qSetCheck = autoTradeOnOff.objects.filter(id=1).first()
        checkOn = model_to_dict(qSetCheck)['auto_trade_is_on']
        if checkOn:
            qSetBatch.text = '現在は、自動取引がONです。最終実行は ' + \
                dt_now.strftime('%Y-%m-%d %H:%M:%S')

        else:
            qSetBatch.text = '現在は、自動取引がOFFです。最終実行は ' + \
                dt_now.strftime('%Y-%m-%d %H:%M:%S')

        qSetBatch.save()
