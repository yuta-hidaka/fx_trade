import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingInfo
import datetime

from oandapyV20 import API


# class s(TemplateView):
#     template_name = "home.html"

def get_current(request):
    # context = super().get_context_data()

    # OANDA API v20の口座IDとAPIトークン
    accountID = "101-009-11457637-001"
    access_token = "46c8cbca4d7b1ed7533cdca8bd0b2eea-ce54c2371b95860a91bc0a977fd923c5"

    # oandaAPI情報
    api = API(access_token=access_token, environment="practice")

    # JSTとUTCの差分
    DIFF_JST_FROM_UTC = -999
    _from = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)

    print('test')

    params = {
        "instruments": "USD_JPY",
        "alignmentTimezone": "Japan",
        'from': _from,
        "count": 24,  # 取得数24
        "granularity": 'H1'  # 1時間足
    }
    pricing_info = PricingInfo(accountID=accountID, params=params)

    try:

        for i in range(1):
            api.request(pricing_info)
            response = pricing_info.response

            prResponse = json.loads(json.dumps(response))
            # context['response'] = prResponse
            prices = prResponse['prices']
            ask_price = prResponse['prices'][0]['asks'][0]['price']
            print(ask_price)
            print(json.dumps(response, indent=2))

            # print(prResponse)
            # print(json.dumps(response, indent=4))  # 出力値を見やすく整形
            # print(i)
            # print(response)

    except V20Error as e:
        print("Error: {}".format(e))

    # data = {'articles': 'responseOKKKKK'}
    return HttpResponse(json.dumps(response), content_type='application/json')
