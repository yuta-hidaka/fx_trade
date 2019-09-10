from django.contrib import admin
# Register your models here.
from .models import autoTradeOnOff, batchRecord, M5_USD_JPY, MA_USD_JPY


admin.site.register(autoTradeOnOff)
admin.site.register(batchRecord)
