from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import (
    M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY,
    conditionOfMA_M5, listConditionOfMA, listConditionOfSlope, condition
)
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *
from django.forms.models import model_to_dict
from ..calculate.compare_ma import compaireMA
from django.core.exceptions import ObjectDoesNotExist
from .set_condition import setCondition


class setMA_USD_JPY:

    def __init__(self):
        self.sCondition = setCondition()

    def setMASlope(self, preveousData, leatestData):
        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        vals = []
        comp = compaireMA()
        # print(preveousData)
        # print(leatestData)
        # print(model_to_dict(preveousData))
        # print(model_to_dict(leatestData))
        ld = model_to_dict(leatestData)
        pd = model_to_dict(preveousData)

        for ma in ListMa:
            key = 'm5_ma' + str(ma)
            data = Decimal(ld[key])-(pd[key])
            vals.append(data)

        create = SlopeM5_USD_JPY.objects.create(
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

        result = self.sCondition.setSlopeComp(vals, leatestData)
        return result

    def setMA(self, FXdata, BBCondi):
        # 変数宣言
        vals = []
        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        is_first = False
        condiSlope = None

        # 現在の最新MA一覧を取得する。
        try:
            leatestData = MA_USD_JPY.objects.latest('created_at')
            # print(FXdata)

        except ObjectDoesNotExist:
            is_first = True
            print('MAの過去データがありません。')
            pass

        for ma in ListMa:
            data = list(M5_USD_JPY.objects.order_by(
                '-recorded_at_utc')[:ma].aggregate(Avg('close')).values())
            vals.append(data[0])

        qSet = MA_USD_JPY
        create = qSet.objects.create(
            m5=FXdata,
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

        # 最初のデータだと傾きを求められないのでパス
        if not is_first:
            # 傾きも求める。
            condiSlope = self.setMASlope(leatestData, create)
            # 短中長期の状態を取得

        # 値比較
        result = self.sCondition.setMAComp(vals, create)

        # 現状を計算した情報を一テーブルに集約
        return self.sCondition.setConditionList(create, result, condiSlope, BBCondi)
