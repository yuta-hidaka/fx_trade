from ...models import batchRecord, autoTradeOnOff, condition, batchLog, assets, tradeSettings
from datetime import datetime, timedelta, timezone
import datetime

from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from ...service.set_candle_USD_JPY import setCandle_USD_JPY
from ...calculate.buy_sell_cal import BuySellCal
from ...service.set_MA_USD_JPY import setMA_USD_JPY
from ...service.set_specific_ma import setSpecificMA

from ...service.set_bollinger_band import setBollingerBand_USD_JPY
from fx_trade_v1_00.lib.order import orderFx
from decimal import *

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
        # text = 'Btrade呼び出されました<br>'

        JST = timezone(timedelta(hours=+9), 'JST')
        dt_now = datetime.datetime.now(JST)
        text = '<p style="color:red;">バッチ起動<br>' + str(dt_now) + '</p><br>'

        # 購買計算オブジェクト
        bsCal = BuySellCal()
        # 設定情報取得
        settings = bsCal.settings
        # ろうそく足データ取得オブジェクト
        setCandle = setCandle_USD_JPY()
        # ボリンジャーバンドオブジェクト
        bb = setBollingerBand_USD_JPY()
        # 平均移動線オブジェクト
        setMA = setMA_USD_JPY()
        # 任意の変数用のオブジェクト
        setSpec = setSpecificMA()
        setSpec.settings = settings
        # オーダーオブジェクト
        order = orderFx()
        # バッチの実行状況を保存する。
        qSetBatch = batchRecord.objects.filter(id=1).first()
        # 自動取引がOFFかONかを確認する。
        qSetCheck = autoTradeOnOff.objects.filter(id=1).first()
        checkOn = model_to_dict(qSetCheck)['auto_trade_is_on']
        # 足の種類
        gran = settings.granularity
        # 通貨ペア
        inst = settings.instruments
        # 短期足
        shortLeg = settings.short_leg
        # 中期足
        middleLeg = settings.middle_leg
        # 長期足
        longLeg = settings.long_leg

        dt_now = datetime.datetime.now(JST)
        text += '<p style="color:red;">一分足の取得<br>' + str(dt_now) + '</p><br>'
        # 5分足の保存
        # result, created = setCandle.setM5()
        # 任意の足保存
        resultSpecific, createdSpecific = setCandle.setSpecific(
            gran=gran, num=1, inst=inst)
        # 1分足の保存
        result, created = setCandle.setM1()

        # UTC時間を取得
        UTC = datetime.datetime.utcnow()
        adjTime = 9
        adjNum = 7
        is_closeMarket = False

        if self.is_dst(UTC):
            adjNum = 6

        # 日本時間取得
        jstMath = UTC + datetime.timedelta(hours=adjTime)
        wk = jstMath.weekday()
        hr = jstMath.hour
        mi = jstMath.minute

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
        setSpec.setMA(resultSpecific)

# '----------------デバッグ用-------------------------------'

        limitMin = [59]
        # 土曜日の6時59分　夏時間で5時59分になったら、ポジションをすべて解除
        if wk == 5 and hr == (adjNum - 1) and mi in limitMin or wk == 5 and hr == adjNum and mi == 0:
            order.allOrderClose()
            text += '土曜日の終了時刻以降になったので取引中止処理を行います。<br>'
            is_closeMarket = True
        # 5分足が作成されたらMAを作成する。
        if created:
            try:
                setSpec.setMA(resultSpecific)
                pass
            except Exception as e:
                print(e)
                pass
            condiPrev = condition.objects.latest('created_at')
            # ------------------------------------------------------------------------------------------------------------------
            dt_now = datetime.datetime.now(JST)
            text += '<p style="color:red;">ボリンジャーバンド計算<br>' + \
                str(dt_now) + '</p><br>'
            # ------------------------------------------------------------------------------------------------------------------
            # ボリンジャーバンドの設定
            BBCondi = bb.setBB(nowMA=result, condiPrev=condiPrev)
            headerText = '<br>----------------------------------------------set bb---------------------------------------------<br>'
            text += (headerText + bb.text + headerText)

            # ------------------------------------------------------------------------------------------------------------------
            dt_now = datetime.datetime.now(JST)
            text += '<p style="color:red;">condition計算<br>' + \
                str(dt_now) + '</p><br>'
            condiNow = setMA.setMA(result, BBCondi)
            # ------------------------------------------------------------------------------------------------------------------
            if not is_closeMarket and checkOn:
                # a = 8
                # ------------------------------------------------------------------------------------------------------------------
                dt_now = datetime.datetime.now(JST)
                text += '<p style="color:red;">by sell cal計算<br>' + \
                    str(dt_now) + '</p><br>'
                # ------------------------------------------------------------------------------------------------------------------
                bsCal.BuySellCheck(condiNow, condiPrev)
                headerText = '<br>----------------------------------------------by sel cal---------------------------------------------<br>'
                text += (headerText + bsCal.text + headerText)
            else:
                text += '自動取引がOFFです。'
                order.allOrderClose()

            ast = order.fi.getAsset()
            astBlance = Decimal(ast['account']['balance'])
            # text += str(ast)
            assets.objects.create(assets=astBlance)

        dt_now = datetime.datetime.now(JST)
        text += '<p style="color:red;">処理終了<br>' + str(dt_now) + '</p>'

        if text != '' and created:
            batchLog.objects.create(text=text)

        qSetBatch.save()
