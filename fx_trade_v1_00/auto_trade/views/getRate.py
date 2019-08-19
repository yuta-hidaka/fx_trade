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


def get_current(request):
    # context = super().get_context_data()

    # OANDA API v20の口座IDとAPIトークン
    accountID = "101-009-11457637-001"
    access_token = "46c8cbca4d7b1ed7533cdca8bd0b2eea-ce54c2371b95860a91bc0a977fd923c5"

    # oandaAPI情報
    api = API(environment="practice", access_token=access_token)

    ########################################################################
    client = API(environment="practice", access_token=access_token)
    # request trades list
    r = trades.TradesList(accountID)
    rv = client.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

    ########################################################################

    params = {
        "instruments": "USD_JPY",
        "alignmentTimezone": "Japan",
        "count": 50,  # 取得数24
        "granularity": 'M5'  # 5分足
    }

    # 過去データリクエスト
    # APIへ過去データをリクエスト

    try:
        r = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
        api.request(r)

    except V20Error as e:
        print("Error: {}".format(e))

    # data = {'articles': 'responseOKKKKK'}
    return HttpResponse(json.dumps(api.request(r)), content_type='application/json')
