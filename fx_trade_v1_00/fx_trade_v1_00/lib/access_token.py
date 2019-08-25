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

# api情報


class FxInfo:
    """API情報取得"""

    def __init__(self):

        is_practice = True
        # is_practice = False
        # OANDA API v20の口座IDとAPIトークン

        self.accountID = "101-009-11457637-001"
        self.access_token = "46c8cbca4d7b1ed7533cdca8bd0b2eea-ce54c2371b95860a91bc0a977fd923c5"

        if is_practice:
            print("practice")
            environment = "practice"
        else:
            print("live")
            environment = "live"

        # oandaAPI情報
        self.api = API(environment=environment, access_token=self.access_token)
