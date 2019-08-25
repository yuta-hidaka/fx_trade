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
# from ..fx_trade_v1_00.lib.access_token import FxInfo


class GetMA:

    def __init__(self):
        self.fx_info = FxInfo()

    def get_MA(self, request):
        api = self.fx_info.api

        params = {
            "instruments": request['instruments'],
            "alignmentTimezone": request['alignmentTimezone'],
            "count": request['count'],
            "granularity": request['granularity']
        }

        # 過去データリクエスト
        # APIへ過去データをリクエスト
        try:
            r = instruments.InstrumentsCandles(
                instrument="USD_JPY", params=params)
            api.request(r)

        except V20Error as e:
            print("Error: {}".format(e))

        return api.request(r)
