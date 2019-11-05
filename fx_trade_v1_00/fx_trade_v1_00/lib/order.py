import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingInfo
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions
from oandapyV20.contrib.requests import (
    MarketOrderRequest, StopLossDetails, TakeProfitOrderRequest
)
from auto_trade.models import batchLog
from .access_token import FxInfo

import oandapyV20.endpoints.instruments as instruments
from django.utils import timezone
import datetime
from auto_trade.models import batchLog,  tradeLog
from oandapyV20 import API

"""
memo
取引情報を確認できる
r = trades.TradeDetails(accountID=accountID, tradeID=49)
api.request(r)

# アカウントのオープントレードを全て取得する
r = trades.OpenTrades(accountID=accountID)
api.request(r)

・initialMarginRequired＝これはトレードが作成された時点の必要なマージン
・MarginUsed＝現時点でのマージン
・realizedPL＝トレードの一部が決済された際の利益/損のトータル
・unrealizedPL＝トレードの未決済状態の利益/損のトータル


 トレードID49の1000通貨のみ決済を行う
r = trades.TradeClose(accountID=accountID, tradeID=49, data=data)
api.request(r)


"""


class orderFx:

    def __init__(self):
        self.now = timezone.now()

        # now = timezone.utc()

        self.fi = FxInfo()
        self.tlog = tradeLog.objects.filter(id=1).first()
        self.isSlock = False
        self.isLlock = False
        # -----------------------------------------------
        # タイムゾーンの生成
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

        # GOOD, タイムゾーンを指定している．早い
        jst = datetime.datetime.now(JST) + datetime.timedelta(minutes=1)
        self.jst = jst.isoformat()+'Z'
        # -----------------------------------------------

        self.now_utc = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        self.now_utc = self.now_utc.isoformat()+'Z'

        # """為替ペア"""
        self.instrument = "USD_JPY"

        # """購買件数マイナスでshort、プラスでlong"""
        self.unitsShort = "-1000"
        # """指値注文"""
        self.priceShort = "109.780"
        # """ストップロスの指定"""
        self.stopLossShort = 100.00

        # """購買件数マイナスでshort、プラスでlong"""
        self.unitsLong = "-1000"
        # """指値注文"""
        self.priceLong = "109.780"
        # """ストップロスの指定"""
        self.stopLossLong = 100.00

        self.data = {
            "order": {
                "price": None,
                "instrument": None,
                "units": None,
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                "stopLossOnFill": None
            }
        }

        # 口座のすべてのポジションをリストとして取得
        r = positions.PositionList(accountID=self.fi.accountID)
        api = self.fi.api
        res = api.request(r)
        pos = res['positions'][0]
        # オーダーステータスを取得する。
        try:
            self.orderLongNum = len(pos['long']['tradeIDs'])
        except:
            self.orderLongNum = 0
        try:
            self.orderShortNum = len(pos['short']['tradeIDs'])
        except:
            self.orderShortNum = 0

    # def getPosition(self):
    def posittionTimeCheck(self):
        now = timezone.now()
        adjTime = datetime.timedelta(minutes=10)
        text = 'positionCheck'
        l_over = False
        s_over = False
        if self.tlog.long_in_time is None:
            self.tlog.long_in_time = now - adjTime

        if self.tlog.short_in_time is None:
            self.tlog.short_in_time = now - adjTime

        shortInTime = self.tlog.short_in_time + adjTime
        longInTime = self.tlog.long_in_time + adjTime
        text += '<br>now '+str(now)
        text += '<br>long in '+str(longInTime)
        text += '<br>shot in '+str(shortInTime)

        if longInTime < now:
            self.isLlock = False
            l_over = True
            text += '<br>long 10分経った'
        else:
            text += '<br>long 10分経ってない'
            self.isLlock = True

        if shortInTime < now:
            text += '<br>short 10分経った'
            self.isSlock = False
            s_over = True
        else:
            text += '<br>short 10分経ってない  '
            self.isSlock = True

        batchLog.objects.create(text=text)
        self.lossCutCheck(l_over, s_over)

    def lossCutCheck(self, l, s):
        # 口座のすべてのポジションをリストとして取得
        # self.tlog = tradeLog.objects.filter(id=1).first()
        r = positions.PositionList(accountID=self.fi.accountID)
        api = self.fi.api
        res = api.request(r)
        pos = res['positions'][0]
        olNum = 0
        osNum = 0
        # オーダーステータスを取得する。
        try:
            olNum = len(pos['long']['tradeIDs'])
        except:
            olNum = 0
        try:
            osNum = len(pos['short']['tradeIDs'])
        except:
            osNum = 0

        # 記録されている情報と現在のポジションを比較する。差があれば損切りされているので、処理を一回休む。
        text = 'loss cut check'

        if self.tlog.long_count == olNum:
            self.isLlock = False
            # text += '<br>ロングおなじ'
        else:
            text += '<br>ロング損切されている　ポジション入れ替え'
            self.ShortOrderCreate()
            if not l and not self.isLlock:
                self.isLlock = True
        
        if self.tlog.short_count == osNum:
            # text += '<br>ショートおなじ'
            self.isSlock = False
        else:
            text += '<br>ショート損切りされている ポジション入れ替え'
            self.ShortOrderCreate()
            if not s and not self.isSlock:
                self.isSlock = True

        self.tlog.short_count = self.orderShortNum
        self.tlog.long_count = self.orderLongNum
        self.tlog.save()
        batchLog.objects.create(text=text)

        if self.isSlock or self.isLlock :
            return True

    def getOrderNum(self):
        # 口座のすべてのポジションをリストとして取得
        self.tlog = tradeLog.objects.filter(id=1).first()
        r = positions.PositionList(accountID=self.fi.accountID)
        api = self.fi.api
        res = api.request(r)
        pos = res['positions'][0]
        # オーダーステータスを取得する。
        try:
            self.orderLongNum = len(pos['long']['tradeIDs'])
        except:
            self.orderLongNum = 0
        try:
            self.orderShortNum = len(pos['short']['tradeIDs'])
        except:
            self.orderShortNum = 0

        # 記録されている情報と現在のポジションを比較する。差があれば損切りされているので、処理を一回休む。
        # text = ''
        # if self.tlog.long_count == self.orderLongNum:
        #     self.isLlock = False
        #     text += '<br>ロングおなじ'
        # else:
        #     text += '<br>ロングちがう'
        #     self.isLlock = True

        # if self.tlog.short_count == self.orderShortNum:
        #     text += '<br>ショートおなじ'
        #     self.isSlock = False
        # else:
        #     text += '<br>ショートちがう  '
        #     self.isSlock = True

        # text += '<br>self.tlog.long_count ' + str(self.tlog.long_count)
        # text += '<br>self.orderLongNum ' + str(self.orderLongNum)
        # text += '<br>self.tlog.short_count ' + str(self.tlog.short_count)
        # text += '<br>self.orderShortNum ' + str(self.orderShortNum)
        # batchLog.objects.create(text=text)

        # self.tlog.short_count = self.orderShortNum
        # self.tlog.long_count = self.orderLongNum
        # self.tlog.save()

    # すべてのポジションを決済します。

    def allOrderClose(self):
        if not self.isSlock and not self.isLlock:
            self.getOrderNum()
            text = 'allOrderClose'
            if self.orderLongNum != 0:
                self.oderCloseAllLong()
            if self.orderShortNum != 0:
                self.oderCloseAllShort()

        batchLog.objects.create(text=text)

    def ShortOrderCreate(self):
        self.posittionTimeCheck()
        text = ''
        flg = False
        text = 'self.isSlock ' + str(self.isSlock) + '<br>'
        if not self.isSlock:
            self.getOrderNum()
            self.oderCloseAllLong()
            text += 'ShortOrderCreate<br>'
            # 今回は1万通貨の買いなので「+10000」としてます。売りの場合は「-10000」と記載です。
            api = self.fi.api
            # stopPrice = 100.00
            stoporder = StopLossDetails(
                price=self.stopLossShort,
                # timeInForce="GTD",
                # gtdTime=self.now_utc
            )

            self.data['order']['price'] = self.priceShort
            self.data['order']['instrument'] = self.instrument
            self.data['order']['units'] = self.unitsShort
            self.data['order']['stopLossOnFill'] = stoporder.data
            # print(self.data)
            # r = trades.TradeClose(accountID=accountID, tradeID=49, data=data)
            # API経由で指値注文を実行
            if self.orderShortNum == 0:
                r = orders.OrderCreate(self.fi.accountID, data=self.data)
                res = api.request(r)
                text += json.dumps(res, indent=2)
                try:
                    self.tlog.short_in_time = self.now
                    self.tlog.save()
                    flg = True
                    pass
                except:
                    text += '購買エラー<br>'
                    pass
        else:
            text += 'short　前回購入しているのに、損切りされているので購買中止<br>'
        return flg

        # self.getOrderNum()
        batchLog.objects.create(text=text)

    def LongOrderCreate(self):
        self.posittionTimeCheck()
        flg = False
        text = 'self.isLlock ' + str(self.isLlock) + '<br>'
        if not self.isLlock:
            self.getOrderNum()
            self.oderCloseAllShort()
            text = 'LongOrderCreate<br>'
            # 今回は1万通貨の買いなので「+10000」としてます。売りの場合は「-10000」と記載です。
            api = self.fi.api
            # stopPrice = 100.00
            stoporder = StopLossDetails(
                price=self.stopLossLong,
                # timeInForce="GTD",
                # gtdTime=self.now_utc
            )

            self.data['order']['price'] = self.priceLong
            self.data['order']['instrument'] = self.instrument
            self.data['order']['units'] = self.unitsLong
            self.data['order']['stopLossOnFill'] = stoporder.data
            # print(self.data)
            # r = trades.TradeClose(accountID=accountID, tradeID=49, data=data)
            # API経由で指値注文を実行
            if self.orderLongNum == 0:

                r = orders.OrderCreate(self.fi.accountID, data=self.data)
                res = api.request(r)
                text += json.dumps(res, indent=2)
                try:
                    self.tlog.long_in_time = self.now
                    self.tlog.save()
                    flg = True
                    pass
                except:
                    text = '購買エラー<br>'
                    pass
            # print(self.data)
            # print(json.dumps(res, indent=2))
            # print('order create----------------------------------------------')
        else:
            text += 'long 前回購入しているのに、損切りされているので購買中止<br>'
        # self.getOrderNum()
        batchLog.objects.create(text=text)
        return flg

    def oderCloseAllLong(self):
        self.getOrderNum()

        text = 'oderCloseAllLong<br>'
        batchLog.objects.create(text=text)
        api = self.fi.api
        """
        longをすべて決済する。
        """
        data = {
            "longUnits": "ALL"
        }
        r = positions.PositionClose(
            accountID=self.fi.accountID,
            instrument=self.instrument,
            data=data
        )

        try:
            if self.orderLongNum != 0:
                api.request(r)
        except:
            print('long決済するデータがありませんでした。')
            pass
        self.tlog.long_count = 0
        self.tlog.save()

    def oderCloseAllShort(self):
        self.getOrderNum()

        text = 'oderCloseAllShort<br>'
        batchLog.objects.create(text=text)
        api = self.fi.api
        """
        shortをすべて決済する。
        """

        data = {
            "shortUnits": "ALL"
        }

        r = positions.PositionClose(
            accountID=self.fi.accountID,
            instrument=self.instrument,
            data=data
        )

        try:
            if self.orderShortNum != 0:
                api.request(r)
        except:
            # print('short決済するデータがありませんでした。')
            pass
        self.tlog.short_count = 0
        self.tlog.save()

    def oderCloseById(self, id):
        self.getOrderNum()

        api = self.fi.api
        """
        id単位で決済する。
        """
        # トレードIDのみ決済を行う
        r = trades.TradeClose(accountID=self.fi.accountID, tradeID=id)
        api.request(r)
