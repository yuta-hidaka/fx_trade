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
from . import views, rest
from .views import getRate, top
# from .rest import getRate

urlpatterns = [
    path('', top.index, name='index'),
    path('M5', top.M5, name='M5'),
    # path('rest', include('rest.urls'), name='rest'),
    # path('getRate', getRate.s.get_current, name='getRate'),
    # path('getRate', top.get_current, name='getRate'),
]
