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


class batch_ma():
    def __init__(self):
        # 50本のM5を取得しておく、その後は連続して更新。
        print("hi")

    def get_current(self, request):
        fx_info = FxInfo()
        test.test()
        print('test')
        api = fx_info.api

        params = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 5000,  # 取得数24
            "granularity": 'M5'  # 5分足
        }

        # 過去データリクエスト
        # APIへ過去データをリクエスト
        try:
            r = instruments.InstrumentsCandles(
                instrument="USD_JPY", params=params)
            api.request(r)

        except V20Error as e:
            print("Error: {}".format(e))

        return HttpResponse(json.dumps(api.request(r)), content_type='application/json')

    def get_MA_5M_5(self):
        print('get_MA_5M_5')

    def get_MA_5M_10(self):
        print('get_MA_5M_10')

    def get_MA_5M_15(self):
        print('get_MA_5M_15')

    def get_MA_5M_20(self):
        print('get_MA_5M_20')
