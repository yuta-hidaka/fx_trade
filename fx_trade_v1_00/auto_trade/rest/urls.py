# """fx_trade_v1_00 URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path, include
from .views import get_rate_API, get_ma_API, trade_switch_API, get_m5vsMa, get_log, trade_settings, get_assets_API
# from . import getRate

urlpatterns = [
    # path('', , name='index'),
    path('getRate', get_rate_API.getRateAPI.as_view(), name='getRate'),
    path('getMA', get_rate_API.getRateAPI.as_view(), name='getMA'),
    path('tradeOnOff', trade_switch_API.tradeOnOffAPI.as_view(), name='tradeOnOff'),
    path('getRate', get_rate_API.getRateAPI.as_view(), name='getRate'),
    path('getLog', get_log.getLogAPI.as_view(), name='getLog'),
    path('M5vsMA', get_m5vsMa.M5vsMaUsdJpyAPI.as_view(), name='M5vsMA'),
    path('getAssets', get_assets_API.getAssetsAPI.as_view(), name='getAssets'),
    path('tradeSettings', trade_settings.tradeSettingsAPI.as_view(),
         name='tradeSettings'),
    path('', get_rate_API.getRateAPI.as_view(), ),
    # path('/getRate', include('auto_trade.urls')),
]
