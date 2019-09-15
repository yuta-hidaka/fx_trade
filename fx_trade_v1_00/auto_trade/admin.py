from django.contrib import admin
# Register your models here.
from .models import (autoTradeOnOff, batchRecord, M5_USD_JPY,
                     MA_USD_JPY, SlopeM5_USD_JPY, conditionOfMA_M5,
                     listConditionOfMA, listConditionOfSlope)


admin.site.register(autoTradeOnOff)
admin.site.register(batchRecord)
admin.site.register(M5_USD_JPY)
admin.site.register(MA_USD_JPY)

admin.site.register(SlopeM5_USD_JPY)
admin.site.register(conditionOfMA_M5)
admin.site.register(listConditionOfMA)
admin.site.register(listConditionOfSlope)
