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

        self.fi = FxInfo()

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

        # # 口座のすべてのポジションをリストとして取得
        # r = positions.PositionList(accountID=self.fi.accountID)
        # api = self.fi.api
        # res = api.request(r)
        # pos = res['positions'][0]
        # # オーダーステータスを取得する。
        # try:
        #     self.orderLongNum = len(pos['long']['tradeIDs'])
        # except:
        #     self.orderLongNum = 0
        # try:
        #     self.orderShortNum = len(pos['short']['tradeIDs'])
        # except:
        #     self.orderShortNum = 0

    def orderNum(self):
        # 口座のすべてのポジションをリストとして取得
        self.tlog = tradeLog.objects.filter(id=1).first()
        self.sCnt = tlog.short_count
        self.lCnt = tlog.long_count
        self.isSlock = False
        self.isLlock = False

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

        if self.sCnt == self.orderLongNum:
            self.isLlock = False
            print('Long OK')
        else:
            self.isLlock = True
            print('Long NG')

        if self.lCnt == self.orderShortNum:
            self.isSlock = False
            print('Short OK')
        else:
            self.isSlock = True
            print('Long NG')

        tlog.short_count = self.orderLongNum
        tlog.long_count = self.orderShortNum
        tlog.save()

        self.text = 'OKkkkkjkkkkk<br>'

    # すべてのポジションを決済します。

    def allOrderClose(self):
        if not self.isSlock and not self.isLlock:
            self.orderNum()
            text = 'allOrderClose'
            if self.orderLongNum != 0:
                self.oderCloseAllLong()
            if self.orderShortNum != 0:
                self.oderCloseAllShort()

        batchLog.objects.create(text=text)

    def ShortOrderCreate(self):
        self.orderNum()
        if not self.isSlock:
            self.oderCloseAllLong()
            text = 'ShortOrderCreate<br>'
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
        else:
            text = 'short　前回購入しているのに、損切りされているので購買中止<br>'

        batchLog.objects.create(text=text)

    def LongOrderCreate(self):
        self.orderNum()
        if not self.isLlock:
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
            # print(self.data)
            # print(json.dumps(res, indent=2))
            print('order create----------------------------------------------')
        else:
            text = 'long 前回購入しているのに、損切りされているので購買中止<br>'

        batchLog.objects.create(text=text)

    def oderCloseAllLong(self):
        self.orderNum()

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

    def oderCloseAllShort(self):
        self.orderNum()

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
            print('short決済するデータがありませんでした。')
            pass

    def oderCloseById(self, id):
        self.orderNum()

        api = self.fi.api
        """
        id単位で決済する。
        """
        # トレードIDのみ決済を行う
        r = trades.TradeClose(accountID=self.fi.accountID, tradeID=id)
        api.request(r)
