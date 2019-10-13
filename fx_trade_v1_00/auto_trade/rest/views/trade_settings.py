import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import tradeSettings
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from auto_trade.service.get_rate_USD_JPY import getFXdata_USD


class tradeSettingsAPI(APIView):

    def get(self, request, format=None):
        result = model_to_dict(tradeSettings.objects.filter(id=1).first())

        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder),
                            content_type='application/json')

    def post(self, request):

        batchLog = ''
        res = (
            batchLog.objects.order_by('-created_at').all().values(
                'id', 'text', 'created_at'
            )[:1000]
        )

        data = {}
        data['result'] = []

        for r in res:
            data['result'].append(r)

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
