import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import batchLog
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from auto_trade.service.get_rate_USD_JPY import getFXdata_USD


class getLogAPI(APIView):

    def get(self, request, format=None):
        print('i')

    def post(self, request):
        startDate = None
        endDate = None
        count = None
        res = (
            batchLog.objects.order_by('-created_at').all().values(
                'id', 'text', 'created_at'
            )[:700]
        )
        data = {}
        data['result'] = []

        for r in res:
            data['result'].append(r)

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
