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
    MarketOrderRequest, StopLossDetails, TakeProfitOrderRequest, TrailingStopLossDetails
)
from auto_trade.models import batchLog
from .access_token import FxInfo

import oandapyV20.endpoints.instruments as instruments
from django.utils import timezone
import datetime
from auto_trade.models import batchLog,  tradeLog
from oandapyV20 import API
from decimal import *
import numpy as np
from time import sleep
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
        self.isLock = False
        self.isReverse = False
        self.nowIn = False
        self.now = timezone.now()
        self.text = ''
#  ma_in_at
        self.isInByMa = False
        # now = timezone.utc()

        self.fi = FxInfo()
        self.tlog = tradeLog.objects.filter(id=1).first()
        self.isSlock = False
        self.isLlock = False
        self.isSlockByTime = False
        self.isLlockByTime = False
        self.waitTime = 0
        self.trend_id = 0
        # 現在の価格
        self.priceNow = 0

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
                # "type": "MARKET",
                "positionFill": "DEFAULT",
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

    def addTrailingOrder(self):
        r = r

    def inByMaCheck(self):
        # maの際は二倍の時間をまつ
        now = timezone.now()
        waitTime = self.waitTime * 2
        trends = [1, 2]
        self.text += '-------------------------inByMaCheck-------------------------<br>'
        if self.trend_id in trends:
            self.text += 'trendなので時間制限持たせません<br>'
            return False

        adjTime = datetime.timedelta(minutes=waitTime * 2)
        if self.isReverse:
            self.text += '----リバース処理なのinmacheck行いません----<br>'
            return

        if self.tlog.ma_in_at is None:
            self.tlog.ma_in_at = now - adjTime

        inMaAt = self.tlog.ma_in_at + adjTime
        self.text += '<br>inMaAt '+str(inMaAt)
        self.text += '<br>self.tlog.ma_in_at '+str(self.tlog.ma_in_at)

        if inMaAt < now:
            self.text += '<br>maの購入より ' + \
                str(self.waitTime)+'分経った inByMaCheck()<br>'
            return False
        else:
            self.text += '<br>lMAの購入より ' + \
                str(self.waitTime)+'分経ってない inByMaCheck()<br>'
            return True

    def positionTimeCheck(self):
        now = timezone.now()
        waitTime = self.waitTime

        adjTime = datetime.timedelta(minutes=waitTime)
        self.text += '-------------------------position time Check-------------------------<br>'
        s_over = False
        l_over = False

        if self.tlog.long_in_time is None:
            self.tlog.long_in_time = now - adjTime

        if self.tlog.short_in_time is None:
            self.tlog.short_in_time = now - adjTime

        shortInTime = self.tlog.short_in_time + adjTime
        longInTime = self.tlog.long_in_time + adjTime

        self.text += '<br>now '+str(now)
        self.text += '<br>long in '+str(longInTime)
        self.text += '<br>shot in '+str(shortInTime)

        if longInTime < now:
            self.isLlockByTime = False
            l_over = True
            self.text += '<br>long '+str(self.waitTime)+'分経った<br>'
        else:
            self.text += '<br>long '+str(self.waitTime)+'分経ってない<br>'
            self.isLlockByTime = True

        if shortInTime < now:
            self.text += '<br>short '+str(self.waitTime)+'分経った<br>'
            self.isSlockByTime = False
            s_over = True
        else:
            self.text += '<br>short '+str(self.waitTime)+'分経ってない <br>'
            self.isSlockByTime = True

        # batchLog.objects.create(self.text=text)
        return s_over, l_over

    def lossCutReverse(self):
        self.text += '<br>-------------------------loss cut reverse-------------------------<'
        self.isReverse = True
        flg = False
        checkRange = [3, 5]
        # トレンドが持ち合いかの時だけ購買
        if self.tlog.condition_id in checkRange:
            so, lo = self.positionTimeCheck()
            # 口座のすべてのポジションをリストとして取得
            self.tlog = tradeLog.objects.filter(id=1).first()
            r = positions.PositionList(accountID=self.fi.accountID)
            self.isLock = True
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

            self.text += '<br>olNum'+str(olNum)+''
            self.text += '<br>self.tlog.long_count' + \
                str(self.tlog.long_count)+'<br>'

            self.text += '<br>osNum'+str(osNum)+''
            self.text += '<br>self.tlog.short_count' + \
                str(self.tlog.short_count)+'<br>'

            # 記録されている情報と現在のポジションを比較する。差があれば損切りされているので、処理を一回休む。
            if self.tlog.long_count != olNum and not lo:
                self.text += '<br>ロング損切されている　position　入れ替え<br>'
                flg = self.ShortOrderCreate()

            if self.tlog.short_count != osNum and not so:
                self.text += '<br><ショート損切りされている position 入れ替え<br>'
                flg = self.LongOrderCreate()

            self.tlog.short_count = self.orderShortNum
            self.tlog.long_count = self.orderLongNum
            self.tlog.save()
            # batchLog.objects.create(text=text)
        else:
            self.text += '<br>購買時のtrend_idが3,5ではなかったのでreverse使いません<br>'
        self.isReverse = False
        return flg

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
        self.text += '<br>loss cut check<br>'

        if self.tlog.long_count == olNum:
            self.isLlock = False
            # self.text += '<br>ロングおなじ'
        else:
            self.text += '<br>-------------------------ロング損切されている----------------------------------<br>'
            if not l and not self.isLlock:
                self.text += '<br> not l and not self.isLlock'
                self.isLlock = True
            elif self.isLock:
                self.text += '<br> self.isLock'
                self.isSlock = True

        if self.tlog.short_count == osNum:
            # self.text += '<br>ショートおなじ'
            self.isSlock = False
        else:
            self.text += '<br>-------------------------ショート損切りされている-------------------------<br>'
            if not s and not self.isSlock:
                self.text += '<br> not s and not self.isSlock<br>'
                self.isSlock = True
            elif self.isLock:
                self.text += '<br> self.isLock<br>'
                self.isSlock = True

        self.tlog.short_count = self.orderShortNum
        self.tlog.long_count = self.orderLongNum
        self.tlog.save()
        # batchLog.objects.create(text=text)

        if self.isSlock or self.isLlock:
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
        # self.text += ''
        # if self.tlog.long_count == self.orderLongNum:
        #     self.isLlock = False
        #     self.text += '<br>ロングおなじ'
        # else:
        #     self.text += '<br>ロングちがう'
        #     self.isLlock = True

        # if self.tlog.short_count == self.orderShortNum:
        #     self.text += '<br>ショートおなじ'
        #     self.isSlock = False
        # else:
        #     self.text += '<br>ショートちがう  '
        #     self.isSlock = True

        # self.text += '<br>self.tlog.long_count ' + str(self.tlog.long_count)
        # self.text += '<br>self.orderLongNum ' + str(self.orderLongNum)
        # self.text += '<br>self.tlog.short_count ' + str(self.tlog.short_count)
        # self.text += '<br>self.orderShortNum ' + str(self.orderShortNum)
        # batchLog.objects.create(self.text=self.text)

        # self.tlog.short_count = self.orderShortNum
        # self.tlog.long_count = self.orderLongNum
        # self.tlog.save()

    # すべてのポジションを決済します。

    def allOrderClose(self):
        if self.nowIn:
            return
        if not self.isSlock and not self.isLlock:
            self.getOrderNum()
            self.text += 'allOrderClose<br>'
            if self.orderLongNum != 0:
                self.oderCloseAllLong()
            if self.orderShortNum != 0:
                self.oderCloseAllShort()

        # batchLog.objects.create(text=text)

    def ShortOrderCreate(self):
        self.text += 'ShortOrderCreate<br>'
        self.oderCloseAllLong()
        # sleep(10)
        # self.text += 'alos<br>'
        # self.text += 'ShortOrderCreate<br>'
        slos = Decimal(self.stopLossShort)
        pNow = Decimal(self.priceNow)

        sld = np.abs(slos - pNow) *-1

        self.text += str(sld)+'差分<br>'
        self.text += str(slos)+'差分<br>'
        self.text += str(pNow)+'差分<br>'

        # if self.nowIn:
        #     self.text += 'short すでに購買済み<br>'
        #     return
        # if self.inByMaCheck():
        #     self.text += 'MA購入から指定時間たってない<br>'
        #     return

        self.positionTimeCheck()
        flg = False
        if not self.isSlockByTime or self.isInByMa:
            self.getOrderNum()
            self.nowIn = True
            api = self.fi.api
            # stopPrice = 100.00
            a = False

            stoporder = TrailingStopLossDetails(distance=str(sld))

            self.data['order']['price'] = self.priceShort
            self.data['order']['instrument'] = self.instrument
            self.data['order']['units'] = self.unitsShort
            self.data['order']['trailingStopLossOnFill'] = stoporder.data
            # print(self.data)
            # r = trades.TradeClose(accountID=accountID, tradeID=49, data=data)
            # API経由で指値注文を実行
            if self.orderShortNum != 0:
                try:
                    now = timezone.now()
                    r = orders.OrderCreate(self.fi.accountID, data=self.data)
                    res = api.request(r)
                    flg = True

                    # maでの購買であれば時間を記録
                    if self.isInByMa:
                        self.text += '<br>short maでの購入です<br>'
                        self.tlog.ma_in_at = now

                    self.tlog.short_in_time = now
                    self.tlog.short_count = 1
                    # 購買時のトレンドを記憶
                    self.tlog.condition_id = self.trend_id
                    self.tlog.save()

                    self.text += json.dumps(res,  indent='<br>')
                    pass
                except Exception as e:
                    self.text += '購買エラー<br>'
                    self.text += str(e)+'<br>'
                    pass
            else:
                self.text += 'ShortOrderCreate行っていません<br>'

        else:
            self.text += str(self.waitTime) + '分経過してない　short<br>'

        # batchLog.objects.create(text=text)
        return flg

        # self.getOrderNum()

    def LongOrderCreate(self):
        self.oderCloseAllShort()
        slos = Decimal(self.stopLossLong)
        pNow = Decimal(self.priceNow)
        # print(slos)
        # print(pNow)
        sld = np.abs(slos - pNow)
        self.text += 'LongOrderCreate<br>'
        self.text += str(sld)+'差分<br>'
        self.text += str(slos)+'差分<br>'
        self.text += str(pNow)+'差分<br>'
        if self.nowIn:
            self.text += 'すでに購買済み<br>'
            return
        if self.inByMaCheck():
            self.text += 'MA購入から指定時間たってない<br>'
            return

        self.positionTimeCheck()
        flg = False
        if not self.isLlockByTime or self.isInByMa:
            self.getOrderNum()
            self.nowIn = True
            api = self.fi.api

            stoporder = TrailingStopLossDetails(distance=str(sld))

            self.data['order']['price'] = self.priceLong
            self.data['order']['instrument'] = self.instrument
            self.data['order']['units'] = self.unitsLong
            self.data['order']['trailingStopLossOnFill'] = stoporder.data
            # print(self.data)
            # r = trades.TradeClose(accountID=accountID, tradeID=49, data=data)
            # API経由で指値注文を実行
            if self.orderLongNum == 0:

                try:
                    now = timezone.now()
                    r = orders.OrderCreate(self.fi.accountID, data=self.data)
                    res = api.request(r)

                    # maでの購買であれば時間を記録
                    if self.isInByMa:
                        self.text += '<br>long maでの購入です<br>'
                        self.tlog.ma_in_at = now

                    self.tlog.long_in_time = now
                    self.tlog.long_count = 1
                    # 購買時のトレンドを記憶
                    self.tlog.condition_id = self.trend_id
                    self.tlog.save()
                    flg = True
                    self.text += json.dumps(res, indent='<br>')
                    pass
                except Exception as e:
                    self.text += '購買エラー<br>'
                    self.text += str(e)+'<br>'
            else:
                self.text += 'LongOrderCreate行っていません<br>'

        else:
            self.text += str(self.waitTime) + '分経過してない　long<br>'
        # self.getOrderNum()
        # batchLog.objects.create(text=text)
        return flg

    def oderCloseAllLong(self):
        if self.nowIn:
            return
        if self.inByMaCheck():
            self.text += 'MA購入から指定時間たってない<br>'
            return

        self.getOrderNum()
        self.text += 'oderCloseAllLong<br>'
        self.text += str(self.isReverse) + 'self.isReverse<br>'
        # batchLog.objects.create(text=text)
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

        if not self.isReverse:
            # 正常に売却したので次回の購買は半分の時間で購入可能にする。
            now = timezone.now()
            adjTime = datetime.timedelta(minutes=(int(self.waitTime / 2)))
            self.tlog.long_in_time = now - adjTime
            self.text += str(self.tlog.long_in_time) + \
                '決済後：self.tlog.long_in_time<br>'
        self.tlog.long_count = 0
        self.tlog.save()

        try:
            if self.orderLongNum != 0:
                api.request(r)
            else:
                self.text += 'long決済してません<br>'
        except:
            # print('long決済するデータがありませんでした。')
            self.text += 'long決済してません　エラーでした<br>'
            pass

    def oderCloseAllShort(self):
        if self.nowIn:
            return
        if self.inByMaCheck():
            self.text += 'MA購入から指定時間たってない<br>'
            return
        self.getOrderNum()
        self.text += 'oderCloseAllShort<br>'
        self.text += str(self.isReverse) + 'self.isReverse<br>'
        # batchLog.objects.create(text=text)
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

        if not self.isReverse:
            # 正常に売却したので次回の購買は半分の時間で購入可能にする。
            adjTime = datetime.timedelta(minutes=(int(self.waitTime / 2)))
            now = timezone.now()
            self.tlog.short_in_time = now - adjTime
            self.text += str(self.tlog.short_in_time) + \
                '決済後：self.tlog.short_in_time<br>'
        self.tlog.short_count = 0
        self.tlog.save()

        try:
            if self.orderShortNum != 0:
                api.request(r)
            else:
                self.text += 'short決済してません<br>'
        except:
            self.text += 'short決済してません　エラーでした<br>'
            # print('short決済するデータがありませんでした。')
            pass

    def oderCloseById(self, id):
        self.getOrderNum()

        api = self.fi.api
        """
        id単位で決済する。
        """
        # トレードIDのみ決済を行う
        r = trades.TradeClose(accountID=self.fi.accountID, tradeID=id)
        api.request(r)
