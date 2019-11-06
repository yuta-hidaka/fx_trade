from ...models import batchRecord, autoTradeOnOff, condition, batchLog, assets
from datetime import datetime, timedelta, timezone

import datetime
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from ...service.set_candle_USD_JPY import setCandle_USD_JPY
from ...calculate.buy_sell_cal import BuySellCal
from ...service.set_MA_USD_JPY import setMA_USD_JPY
from ...service.set_bollinger_band import setBollingerBand_USD_JPY
from ...service.set_candle_USD_JPY import setCandle_USD_JPY
from fx_trade_v1_00.lib.order import orderFx
from decimal import *

import datetime
import pytz


# BaseCommandを継承して作成


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'auto trade batch'

    def is_dst(self, time):
        dt0 = time
        tz0 = pytz.timezone('Asia/Tokyo')
        tz1 = pytz.timezone('US/Eastern')
        dt1 = tz0.localize(dt0).astimezone(tz1)
        return(dt1.dst().seconds > 0)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        text = ''
        JST = timezone(timedelta(hours=+9), 'JST')
        dt_now = datetime.datetime.now(JST)
        setCandle = setCandle_USD_JPY()
        bsCal = BuySellCal()
        # バッチの実行状況を保存する。
        qSetBatch = batchRecord.objects.filter(id=1).first()
        # 5分足の保存
        # result, created = setCandle.setM5()
        # 1分足の保存
        result, created = setCandle.setM1()

        bb = setBollingerBand_USD_JPY()
        setMA = setMA_USD_JPY()
        order = orderFx()
        order = orderFx()
        UTC = datetime.datetime.utcnow()
        adjTime = 9
        adjNum = 7
        is_closeMarket = False

        # isDst =
        if self.is_dst(UTC):
            adjNum = 6

        # 自動取引がOFFかONかを確認する。
        qSetCheck = autoTradeOnOff.objects.filter(id=1).first()
        checkOn = model_to_dict(qSetCheck)['auto_trade_is_on']
        # 日本時間取得
        jstMath = UTC + datetime.timedelta(hours=adjTime)

        # 土曜日の6時55分　夏時間で5時55分になってら、ポジションをすべて解除
        wk = jstMath.weekday()
        hr = jstMath.hour
        mi = jstMath.minute

        # else:
        # text += '土曜日の終了時刻以降になったので取引中止処理を行います。<br>'

        # text += '現在時刻上からweek、hour、adjsttime, min　、5だと土曜日、6:55をチェック<br>'
        # text += str(jstMath.weekday())+'　→　jstMath.weekday()<br>'
        # text += str(jstMath.weekday() == 5)+'　→　jstMath.weekday() == 5<br>'
        # text += str(jstMath.hour)+'　→　jstMath.hour<br>'
        # text += str(jstMath.hour == adjNum)+'　→　jstMath.hour == adjNum<br>'
        # text += str(adjNum)+'　→　adjNum<br>'
        # text += str(jstMath.minute)+'　→　jstMath.minute<br>'
        # text += str(jstMath.minute >= 55)+'　→　jstMath.minute >= 55<br>'
        # conditionListをもとに売買ポイントを考える。

        if checkOn:
            qSetBatch.text = '現在は、自動取引がONです。最終実行は ' + \
                dt_now.strftime('%Y-%m-%d %H:%M:%S')
        else:
            qSetBatch.text = '現在は、自動取引がOFFです。最終実行は ' + \
                dt_now.strftime('%Y-%m-%d %H:%M:%S')

# '----------------デバッグ用-------------------------------'
        # condiPrev = condition.objects.latest('created_at')
        # bb = setBollingerBand_USD_JPY()
        # BBCondi = bb.setBB(nowMA=result, condiPrev=condiPrev)
        # setMA = setMA_USD_JPY()
        # condiNow = setMA.setMA(result, BBCondi)
        # bsCal.BuySellCheck(condiNow, condiPrev)
# '----------------デバッグ用-------------------------------'

        limitMin = [58, 59]
        if wk == 5 and hr == (adjNum - 1) and mi in limitMin or wk == 5 and hr == adjNum and mi == 0:
            order.allOrderClose()
            text += '土曜日の終了時刻以降になったので取引中止処理を行います。<br>'
            is_closeMarket = True
        # 5分足が作成されたらMAを作成する。
        if created:
            condiPrev = condition.objects.latest('created_at')
            # ボリンジャーバンドの設定
            BBCondi = bb.setBB(nowMA=result, condiPrev=condiPrev)
            condiNow = setMA.setMA(result, BBCondi)
            if not is_closeMarket and checkOn:
                # a = 8
                bsCal.BuySellCheck(condiNow, condiPrev)
            else:
                text += '自動取引がOFFです。'
                order.allOrderClose()

            ast = order.fi.getAsset()
            ast = Decimal(ast['account']['balance'])
            assets.objects.create(assets=ast)

        if text != '':
            batchLog.objects.create(text=text)

        qSetBatch.save()
