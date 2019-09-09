import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from auto_trade.service.get_MA_USD import getMA_USD


class getMaAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        gMA_USD = getMA_USD()

        data = ""

        print('hi')
        print(data)

        return HttpResponse(json.dumps(data), content_type='application/json')
