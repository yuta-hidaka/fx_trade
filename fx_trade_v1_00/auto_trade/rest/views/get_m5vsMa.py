import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import conditionOfMA_M5
from django.forms.models import model_to_dict

from django.http import JsonResponse

from auto_trade.service.get_rate_USD_JPY import getFXdata_USD

from django.core import serializers


class M5vsMaUsdJpyAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):

        res = {}
        res['condMa'] = []
        res['ma'] = []
        res['m5'] = []

        result = conditionOfMA_M5.objects.prefetch_related(
            'ma'
        ).order_by(
            '-id'
        )[:500]

        c = result.count()

        for r in result:
            if not r.ma.m5 == None:
                res['count'].append(c)
                res['condMa'].append(model_to_dict(r))
                res['ma'].append(model_to_dict(r.ma))
                res['m5'].append(model_to_dict(r.ma.m5))

        return JsonResponse(res, safe=False)

    def date_handler(obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

# print json.dumps(data, default=date_handler)
