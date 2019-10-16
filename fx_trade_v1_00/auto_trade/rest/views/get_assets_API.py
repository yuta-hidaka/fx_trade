import json
import time
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import assets
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


class getAssetsAPI(APIView):

    def get(self, request, format=None):
        print('hi')

    def post(self, request):

        res = (
            assets.objects.order_by('-created_at').all().values(
                'assets', 'created_at'
            )[:1000].distinct('assets')
        )

        data = {}
        data['result'] = []

        for r in res:
            data['result'].append(r)
        data['result'].reverse()

        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
