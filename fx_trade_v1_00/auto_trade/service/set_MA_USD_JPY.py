from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, MA_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *


class setMA_USD_JPY:

    def setMA(self):

        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        getcontext().prec = 8
        vals = []

        for ma in ListMa:
            data = list(M5_USD_JPY.objects.order_by(
                '-recorded_at_utc')[:ma].aggregate(Avg('close')).values())
            vals.append(data[0])

            print(Decimal(str(data[0]))+Decimal(str(0)))

        qSet = MA_USD_JPY
        qSet.objects.create(
            m5_ma5=vals[0],
            m5_ma10=vals[1],
            m5_ma12=vals[1],
            m5_ma15=vals[2],
            m5_ma20=vals[3],
            m5_ma24=vals[3],
            m5_ma30=vals[4],
            m5_ma36=vals[4],
            m5_ma40=vals[5],
            m5_ma50=vals[6],
            m5_ma70=vals[7],
            m5_ma72=vals[7],
            m5_ma75=vals[8],
            m5_ma140=vals[9],
            m5_ma144=vals[9],
            m5_ma150=vals[10],
            m5_ma288=vals[11]
        )
