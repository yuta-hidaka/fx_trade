from ...models import batchRecord, autoTradeOnOff
from datetime import datetime, timedelta, timezone

import datetime
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from ...service.set_candle_USD_JPY import setCandle_USD_JPY
from ...service.set_MA_USD_JPY import setMA_USD_JPY
from auto_trade.service.set_candle_USD_JPY import setCandle_USD_JPY

# BaseCommandを継承して作成


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'auto trade batch'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        dt_now = datetime.datetime.now(JST)
        # バッチの実行状況を保存する。
        qSetBatch = batchRecord.objects.filter(id=1).first()

        # 5分足の保存
        setCandle = setCandle_USD_JPY()
        result, created = setCandle.setM5()

        # 5分足が作成されたらMAを作成する。
        if created:
            setMA = setMA_USD_JPY()
            setMA.setMA(result)
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
