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
        res = {}
        res['bb'] = []

        result = condition.objects.prefetch_related().order_by(
            '-created_at'
        )[:500]

        c = result.count()

        try:
            for r in result:
                res['bb'].append(model_to_dict(r.condition_of_bb.bb))

        except:
            print('hik')
            pass

        return JsonResponse(res, safe=False)

    def post(self, request):
        # デバッグ用
        # c = Command()
        # a = c.handle()

        res = {}
        res['condMa'] = []
        res['condSlope'] = []
        res['condBB'] = []
        res['bb'] = []
        res['ma'] = []
        res['m5'] = []

        result = condition.objects.prefetch_related().order_by(
            '-created_at'
        )[:500]

        c = result.count()

        try:
            for r in result:
                if not r.ma.m5 == None and not r.condition_of_bb == None:
                    res['condSlope'].append(
                        model_to_dict(r.condition_of_slope_M5))
                    res['condMa'].append(model_to_dict(r.condition_of_ma_M5))
                    res['condBB'].append(model_to_dict(r.condition_of_bb))
                    res['bb'].append(model_to_dict(r.condition_of_bb.bb))
                    res['ma'].append(model_to_dict(r.ma))
                    res['m5'].append(model_to_dict(r.ma.m5))
        except:
            print('hik')

            pass

        return JsonResponse(res, safe=False)


# print json.dumps(data, default=date_handler)
