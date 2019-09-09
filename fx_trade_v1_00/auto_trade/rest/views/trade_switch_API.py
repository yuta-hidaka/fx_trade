import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from auto_trade.service.get_MA_USD import getMA_USD
from ...models import autoTradeOnOff
from django.http import HttpResponse
from ...service.get_MA_USD import getMA_USD
from ..serializers.trade_switch_Serializer import AutoTradeOnOffSerializer


class tradeOnOffAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        qSet = autoTradeOnOff.objects.filter(id=1).first()

        a = self.request.data.dict()

        serializer = AutoTradeOnOffSerializer(data=a)

        if(serializer.is_valid()):
            serializer.update()
        else:
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        gMA = getMA_USD()

        if(self.request.data['auto_trade_is_on'] == 1):
            qSet.auto_trade_is_on = True
            qSet.save()
            gMA.getMA_5_20_75
        else:
            qSet.auto_trade_is_on = False
            qSet.save()

        return HttpResponse('')


class realTradeOnOffAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        gMA_USD = getMA_USD()

        data = ""

        print('hi')
        print(data)

        return HttpResponse(json.dumps(data), content_type='application/json')
