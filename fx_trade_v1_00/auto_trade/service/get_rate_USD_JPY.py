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


class getFXdata_USD():

    def get_current(self, request):
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
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 1,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_5(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 5,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_10(self):

        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 10,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_15(self):

        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 15,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_20(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 20,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_50(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 50,
            "granularity": 'M5'
        }

        return self.get_current(parm)

    def get_5M_250(self):
        parm = {
            "instruments": "USD_JPY",
            "alignmentTimezone": "Japan",
            "count": 250,
            "granularity": 'M5'
        }

        return self.get_current(parm)
