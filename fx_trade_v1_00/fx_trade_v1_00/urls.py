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
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'FX自動取引管理画面'
admin.site.index_title = 'メニュー'


urlpatterns = [
    path('auto_trade/', include('auto_trade.urls')),
    # path('auto_trade/rest', include('auto_trade.rest.urls')),
    path('', include('auto_trade.urls')),
    path('admin/', admin.site.urls),
]
