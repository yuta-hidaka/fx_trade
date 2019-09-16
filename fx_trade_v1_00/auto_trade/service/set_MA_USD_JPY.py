from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import (
    M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY,
    conditionOfMA_M5, listConditionOfMA, listConditionOfSlope
)
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *
from django.forms.models import model_to_dict
from ..calculate.compare_ma import compaireMA


class setMA_USD_JPY:

    def setMASlope(self, preveousData, leatestData):
        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        vals = []

        # print(model_to_dict(preveousData))
        # print(model_to_dict(leatestData))

        for ma in ListMa:
            key = 'm5_ma'+str(ma)
            data = Decimal(model_to_dict(leatestData)[
                           key])-(model_to_dict(preveousData)[key])
            vals.append(data)

        qSet = SlopeM5_USD_JPY
        create = qSet.objects.create(
            ma_previous=preveousData,
            ma_leatest=leatestData,
            slope_m5_ma5=vals[0],
            slope_m5_ma6=vals[1],
            slope_m5_ma10=vals[2],
            slope_m5_ma12=vals[3],
            slope_m5_ma15=vals[4],
            slope_m5_ma20=vals[5],
            slope_m5_ma24=vals[6],
            slope_m5_ma30=vals[7],
            slope_m5_ma36=vals[8],
            slope_m5_ma40=vals[9],
            slope_m5_ma50=vals[10],
            slope_m5_ma70=vals[11],
            slope_m5_ma72=vals[12],
            slope_m5_ma75=vals[13],
            slope_m5_ma140=vals[14],
            slope_m5_ma144=vals[15],
            slope_m5_ma150=vals[16],
            slope_m5_ma288=vals[17]
        )

    def setMA(self):

        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        # 値比較
        comp = compaireMA()
        print('hhdddgggggh')
        is_first = False

        # 現在の最新MA一覧を取得する。
        try:
            leatestData = MA_USD_JPY.objects.latest('created_at')
        except expression as identifier:
            is_first = True
            print('MAの過去データがありません。')
            pass

        print('hhh6')

        # 変数宣言
        vals = []
        print('hhhddd')

        for ma in ListMa:
            data = list(M5_USD_JPY.objects.order_by(
                '-recorded_at_utc')[:ma].aggregate(Avg('close')).values())
            vals.append(data[0])
        print('hhh')

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

        print('hhhkgkg')

        # 差所のデータだと傾きを求められないのでパス
        if not is_first:
            # 傾きも求める。
            self.setMASlope(leatestData, create)
            # 短中長期の状態を取得
            print('hhhkgkrrrrg')

        # ma_comp5_20_75
        resultComp1 = comp.comp3MA(vals[0], vals[5], vals[13])
        # ma_comp6_24_72
        resultComp2 = comp.comp3MA(vals[1], vals[6], vals[12])
        print('hhhkgkggggggggg')

        # 状態に関連するobject取得
        rComp1 = listConditionOfMA.objects.filter(id=resultComp1).first()
        rComp2 = listConditionOfMA.objects.filter(id=resultComp2).first()
        print('hhhkgddddddddddddddddddkg')

        qSetCondition = conditionOfMA_M5
        qSetCondition.objects.create(
            ma_comp5_20_75=rComp1,
            ma_comp6_24_72=rComp2,
            ma=create
        )
        print('hhhdddddddddddddddddddddddddddddddddddddddddddddddddkgkg')

        # print('resultComp1')
        # print(vals[0])
        # print(vals[5])
        # print(vals[13])
        # print('resultComp1')
        # print(resultComp2)
        # print(vals[1])
        # print(vals[6])
        # print(vals[12])

        # print(leatestData)
        # print(create)
