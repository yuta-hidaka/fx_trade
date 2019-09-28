import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import conditionOfMA_M5, condition
from django.forms.models import model_to_dict
from django.http import JsonResponse
from ...service.get_rate_USD_JPY import getFXdata_USD
from django.core import serializers

from ...management.commands.BatchTradeStart import Command

# from ....fx_trade_v1_00.lib.order import orderFx
from fx_trade_v1_00.lib.order import orderFx


class M5vsMaUsdJpyAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        # デバッグ用
        # c = Command()
        # a = c.handle()

        res = {}
        res['condMa'] = []
        res['condSlope'] = []
        res['ma'] = []
        res['m5'] = []

        result = condition.objects.prefetch_related().order_by(
            '-created_at'
        )[:1500]

        c = result.count()
        try:
            for r in result:
                if not r.ma.m5 == None:
                    res['condSlope'].append(
                        model_to_dict(r.condition_of_slope_M5))
                    res['condMa'].append(model_to_dict(r.condition_of_ma_M5))
                    res['ma'].append(model_to_dict(r.ma))
                    res['m5'].append(model_to_dict(r.ma.m5))
        except:
            pass

        # a = orderFx()
        # l = a.orderCreate()

        return JsonResponse(res, safe=False)


# print json.dumps(data, default=date_handler)
