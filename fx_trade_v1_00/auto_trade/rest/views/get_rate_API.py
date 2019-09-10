import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from auto_trade.service.get_rate_USD_JPY import getFXdata_USD


class getRateAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        gFXdata_USD = getFXdata_USD()

        data = gFXdata_USD.get_5M_1()

        print('hi')
        print(data)


        return HttpResponse(json.dumps(data), content_type='application/json')
