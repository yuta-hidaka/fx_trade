from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *
from django.forms.models import model_to_dict


class setMA_USD_JPY:

    def setMASlope(self, preveousData, leatestData):
        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        vals = []

        # print(model_to_dict(preveousData))
        # print(model_to_dict(leatestData))

        ma_previous

        for ma in ListMa:
            key = 'm5_ma'+str(ma)
           data=Decimal(model_to_dict(leatestData)[key])-(model_to_dict(preveousData)[key])
            vals.append(data[0])
            
        create = qSet.objects.create(
            m5_ma5=vals[0],
            m5_ma6=vals[1],
            m5_ma10=vals[2],
            m5_ma12=vals[3],
            m5_ma15=vals[4],
            m5_ma20=vals[5],
            m5_ma24=vals[6],
            m5_ma30=vals[7],
            m5_ma36=vals[8],
            m5_ma40=vals[9],
            m5_ma50=vals[10],
            m5_ma70=vals[11],
            m5_ma72=vals[12],
            m5_ma75=vals[13],
            m5_ma140=vals[14],
            m5_ma144=vals[15],
            m5_ma150=vals[16],
            m5_ma288=vals[17]
        )

    def setMA(self):

        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]

        # 現在の最新MA一覧を取得する。
        leatestData = MA_USD_JPY.objects.latest('created_at')
        # 変数宣言
        vals = []

        for ma in ListMa:
            data = list(M5_USD_JPY.objects.order_by(
                '-recorded_at_utc')[:ma].aggregate(Avg('close')).values())
            vals.append(data[0])

        qSet = MA_USD_JPY
        create = qSet.objects.create(
            m5_ma5=vals[0],
            m5_ma6=vals[1],
            m5_ma10=vals[2],
            m5_ma12=vals[3],
            m5_ma15=vals[4],
            m5_ma20=vals[5],
            m5_ma24=vals[6],
            m5_ma30=vals[7],
            m5_ma36=vals[8],
            m5_ma40=vals[9],
            m5_ma50=vals[10],
            m5_ma70=vals[11],
            m5_ma72=vals[12],
            m5_ma75=vals[13],
            m5_ma140=vals[14],
            m5_ma144=vals[15],
            m5_ma150=vals[16],
            m5_ma288=vals[17]
        )

        # 傾きも求める。
        self.setMASlope(leatestData, create)

        # print(leatestData)
        # print(create)
