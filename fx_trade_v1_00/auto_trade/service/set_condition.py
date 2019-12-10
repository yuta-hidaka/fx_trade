from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import (
    M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY,
    conditionOfMA_M5, conditionOfSlope_M5,
    listConditionOfMA, listConditionOfSlope,
    condition

)
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *
from django.forms.models import model_to_dict
from ..calculate.compare_ma import compaireMA
from django.core.exceptions import ObjectDoesNotExist


class setCondition:
    def setSlopeComp(self, vals, create):
        comp = compaireMA()
        m5_1 = Decimal(model_to_dict(create.m5)['close'])
        # ma_comp5_20_75
        resultComp1 = comp.comp3MASlope(vals[0], vals[5], vals[13])
        # ma_comp6_24_72
        resultComp2 = comp.comp3MASlope(vals[1], vals[6], vals[12])
        # ma_comp6_24_72
        resultComp3 = comp.comp3MASlope(vals[0], vals[5], vals[9])
        # ma_comp6_24_72
        resultComp4 = comp.comp3MASlope(vals[1], vals[6], vals[10])
        # ma_comp1_6_24
        resultComp5 = comp.comp3MASlope(m5_1, vals[1], vals[6])
        # ma_comp1_6_24
        resultComp6 = comp.comp3MASlope(vals[7], vals[14], vals[17])

        # 状態に関連するobject取得
        rComp1 = listConditionOfSlope.objects.filter(id=resultComp1).first()
        rComp2 = listConditionOfSlope.objects.filter(id=resultComp2).first()
        rComp3 = listConditionOfSlope.objects.filter(id=resultComp3).first()
        rComp4 = listConditionOfSlope.objects.filter(id=resultComp4).first()
        rComp5 = listConditionOfSlope.objects.filter(id=resultComp5).first()
        rComp6 = listConditionOfSlope.objects.filter(id=resultComp6).first()
        # print(rComp1)

        result = conditionOfSlope_M5.objects.create(
            slope_comp5_20_75=rComp1,
            slope_comp5_20_40=rComp3,
            slope_comp6_24_72=rComp2,
            slope_comp6_24_50=rComp4,
            slope_comp1_6_24=rComp5,
            slope_comp24_75_288=rComp6,
            ma=create
        )
        return result

    def setMAComp(self, vals, create):

        # [5, 6, 10, 12, 15, 20, 24, 30, 36, 40, 50, 70, 72, 75, 140, 144, 150, 288]
        # [1, 2,  3,  4,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,  16,  17,  18,  19]

        comp = compaireMA()
        m5_1 = Decimal(model_to_dict(create.m5)['close'])
        # ma_comp5_20_75
        resultComp1 = comp.comp3MA(vals[0], vals[5], vals[13])
        # ma_comp5_20_40
        resultComp2 = comp.comp3MA(vals[1], vals[6], vals[12])
        # ma_comp6_24_72
        resultComp3 = comp.comp3MA(vals[0], vals[5], vals[9])
        # ma_comp6_24_50
        resultComp4 = comp.comp3MA(vals[1], vals[6], vals[10])
        # ma_comp1_6_24
        resultComp5 = comp.comp3MA(m5_1, vals[1], vals[6])
        # ma_comp24_75_288
        resultComp6 = comp.comp3MA(vals[7], vals[14], vals[17])

        # 状態に関連するobject取得
        rComp1 = listConditionOfMA.objects.filter(id=resultComp1).first()
        rComp2 = listConditionOfMA.objects.filter(id=resultComp2).first()
        rComp3 = listConditionOfMA.objects.filter(id=resultComp3).first()
        rComp4 = listConditionOfMA.objects.filter(id=resultComp4).first()
        rComp5 = listConditionOfMA.objects.filter(id=resultComp5).first()
        rComp6 = listConditionOfMA.objects.filter(id=resultComp6).first()

        result = conditionOfMA_M5.objects.create(
            ma_comp5_20_75=rComp1,
            ma_comp5_20_40=rComp3,
            ma_comp6_24_72=rComp2,
            ma_comp6_24_50=rComp4,
            ma_comp1_6_24=rComp5,
            ma_comp24_75_288=rComp6,
            ma=create
        )
        return result

    def setConditionList(self, FXdata, BBCondi):
    
        create = condition.objects.create(
            mas=FXdata,
            # condition_of_slope_M5=slope,
            # condition_of_ma_M5=macomp,
            condition_of_bb=BBCondi
        )

        return create
