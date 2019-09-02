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
from .getRate import getFXdata_USD as a

print(a.get_MA_5M_1)
print(a.get_MA_5M_5)
print(a.get_MA_5M_10)
print(a.get_MA_5M_15)
print(a.get_MA_5M_20)
print(a.get_MA_5M_50)
# print(a.get_MA_5M_50)


class getFXdata_USD():

    def get_current(self, request):
        fx_info = FxInfo()
        test.test()
        print('test')
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

    def get_MA_5M_1(self):
        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 1,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_MA_5M_5(self):
        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 5,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_MA_5M_10(self):
        print('get_MA_5M_10')

        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 10,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_MA_5M_15(self):
        print('get_MA_5M_15')

        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 15,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_MA_5M_20(self):
        print('get_MA_5M_20')

        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 20,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_MA_5M_50(self):
        print('get_MA_5M_20')

        print('get_MA_5M_5')
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 50,
            "granularity": 'M5'
        }

        return self.get_current(parm)
