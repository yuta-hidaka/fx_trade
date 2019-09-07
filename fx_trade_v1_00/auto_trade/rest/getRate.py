import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.get_rate_USD import getFXdata_USD


class getRateAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):
        getFXdata_USD.get_current

        print('hi')
        print(getFXdata_USD.get_current)

        return HttpResponse(json.dumps(getFXdata_USD.get_current), content_type='application/json')
