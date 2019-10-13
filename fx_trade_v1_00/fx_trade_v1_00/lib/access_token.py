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
from auto_trade.models import tradeSettings, batchLog


from oandapyV20 import API

# api情報


class FxInfo:
    """API情報取得"""

    def __init__(self):
        setting = tradeSettings.objects.filter(id=1).first()
        text = ''

        is_practice = True
        # is_practice = False
        # OANDA API v20の口座IDとAPIトークン

        self.accountID = ""
        self.access_token = ""

        if not setting.on_real_trade:
            self.accountID = setting.practiceId
            self.access_token = setting.practiceToken
            # print("practice")
            environment = "practice"
        else:
            # print("live")
            environment = "live"
            self.accountID = setting.realId
            self.access_token = setting.realToken

        # text = str(setting.on_real_trade)
        # text += str(self.accountID)
        # text += str(self.access_token)

        # oandaAPI情報
        try:
            self.api = API(environment=environment,
                           access_token=self.access_token)
            pass
        except:
            text = 'OANDA APIから情報の取得に失敗しました。'
            pass

        if text != '':
            batchLog.objects.create(text=text)
