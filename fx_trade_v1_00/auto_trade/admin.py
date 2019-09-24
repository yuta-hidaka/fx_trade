from django.contrib import admin
# Register your models here.
from .models import (
    autoTradeOnOff, batchRecord, M5_USD_JPY,
    MA_USD_JPY, SlopeM5_USD_JPY, conditionOfMA_M5, conditionOfSlope_M5,
    listConditionOfMA, listConditionOfSlope, condition, sellBuyAlert
)


class DateTime(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )


admin.site.register(orderStatus, DateTime)
admin.site.register(autoTradeOnOff, DateTime)
admin.site.register(sellBuyAlert, DateTime)
admin.site.register(condition, DateTime)

admin.site.register(batchRecord, DateTime)
admin.site.register(M5_USD_JPY, DateTime)
admin.site.register(MA_USD_JPY, DateTime)

admin.site.register(SlopeM5_USD_JPY, DateTime)
admin.site.register(conditionOfMA_M5, DateTime)
admin.site.register(conditionOfSlope_M5, DateTime)

admin.site.register(listConditionOfMA, DateTime)
admin.site.register(listConditionOfSlope, DateTime)
