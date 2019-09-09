from django.contrib import admin
# Register your models here.
from .models import autoTradeOnOff, batchRecord


admin.site.register(autoTradeOnOff)
admin.site.register(batchRecord)
