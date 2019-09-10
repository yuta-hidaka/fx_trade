import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from auto_trade.service.get_MA_USD_JPY import getMA_USD_JPY
from ...models import autoTradeOnOff
from django.http import HttpResponse
from ...service.get_MA_USD_JPY import getMA_USD_JPY
from ..serializers.trade_switch_Serializer import AutoTradeOnOffSerializer


class tradeOnOffAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        qSet = autoTradeOnOff.objects.filter(id=1).first()

        # serializer = AutoTradeOnOffSerializer(
        #     data=self.request.data)

        # gMA = getMA_USD_JPY()

        if(self.request.data['auto_trade_is_on'] == 'true'):
            qSet.auto_trade_is_on = True
            qSet.save()
            # gMA.getMA_5_20_75
        else:
            qSet.auto_trade_is_on = False
            qSet.save()

        return HttpResponse('')


class realTradeOnOffAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        gMA_USD = getMA_USD_JPY()

        data = ""

        print('hi')
        print(data)

        return HttpResponse(json.dumps(data), content_type='application/json')
