import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingInfo
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.trades as trades
import datetime
from oandapyV20 import API
from fx_trade_v1_00.lib.access_token import FxInfo
from fx_trade_v1_00.lib import test
import time
import datetime
from pytz import timezone
from ..models import autoTradeOnOff


class getMA_USD_JPY():
    def __init__(self):
        # print('getMA_USD_JPY')
        self.localTime = (
            datetime.datetime.now(timezone('UTC')) -
            datetime.timedelta(minutes=5)
        ).isoformat()

        self.localTime_m1 = (
            datetime.datetime.now(timezone('UTC')) -
            datetime.timedelta(minutes=1)
        ).isoformat()

        self.dayAgo = (
            datetime.datetime.now(timezone('UTC')) -
            datetime.timedelta(days=1)
        ).isoformat()

        # print(self.localTime)
        # self.MA250 = self.get_5M_250()

    def getMA_5_20_75(self):
        MA250 = self.MA250
        # print(MA250)

        while autoTradeOnOff.objects.filter(id=1):
            print('hello')
            time.sleep(1)

    def get_MA(self, request):
        fx_info = FxInfo()
        api = fx_info.api

        params = request

        # 過去データリクエスト
        # APIへ過去データをリクエスト
        try:
            r = instruments.InstrumentsCandles(
                instrument="USD_JPY", params=params)
            api.request(r)

        except V20Error as e:
            print("Error: {}".format(e))

        return api.request(r)

        # return HttpResponse(json.dumps(api.request(r)), content_type='application/json')

    def get_D_20(self):
        parm = {
            # "from": self.dayAgo,
            "to": self.dayAgo,
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 20,
            "granularity": 'D'
        }

        return self.get_MA(parm)

    def get_now(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 1,
            "granularity": 'S5'
        }

        return self.get_MA(parm)

    def get_1M_num(self,  cnt):
        parm = {
            "from": self.localTime_m1,
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": str(cnt),
            "granularity": 'M1'
        }

        return self.get_MA(parm)

    def get_5M_1(self):
        parm = {
            "from": self.localTime,
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 1,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_5(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 5,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_10(self):

        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 10,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_15(self):

        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 15,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_20(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 20,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_num(self, num):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": num,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_25(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 25,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_50(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 50,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_250(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 250,
            "granularity": 'M5'
        }

        return self.get_MA(parm)
