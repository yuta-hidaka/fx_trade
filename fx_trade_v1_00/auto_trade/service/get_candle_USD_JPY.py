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

from ..models import autoTradeOnOff


class getandle_USD():
    def __init__(self):
        self.MA250 = self.get_5M_250()

    def getMA_5_20_75(self):
        MA250 = self.MA250
        print(MA250)

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

    def get_5M_1(self):
        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 1,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_5(self):
        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 5,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_10(self):
        print('get_MA_5M_10')

        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 10,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_15(self):
        print('get_MA_5M_15')

        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 15,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_20(self):
        print('get_MA_5M_20')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 20,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_50(self):
        print('get_MA_5M_20')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 50,
            "granularity": 'M5'
        }

        return self.get_MA(parm)

    def get_5M_250(self):
        print('get_MA_5M_20')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 250,
            "granularity": 'M5'
        }

        return self.get_MA(parm)
