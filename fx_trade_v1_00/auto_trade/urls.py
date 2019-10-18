"""fx_trade_v1_00 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import getRate, top
# from .rest import getRate

urlpatterns = [
    path('', top.index, name='index'),
    path('M5/', top.M5, name='M5'),
    path('m5vsMaComp/', top.m5vsMaComp, name='m5vsMaComp'),
    path('bb/', top.bb, name='bb'),
    path('Log/', top.log, name='log'),
    path('assets/', top.assets, name='assets'),

    # path('rest', rest.urls),
    path('rest/', include('auto_trade.rest.urls')),

    # path('getRate', getRate.s.get_current, name='getRate'),
    # path('getRate', top.get_current, name='getRate'),
]
