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

        # 状態に関連するobject取得
        rComp1 = listConditionOfSlope.objects.filter(id=resultComp1).first()
        rComp2 = listConditionOfSlope.objects.filter(id=resultComp2).first()
        rComp3 = listConditionOfSlope.objects.filter(id=resultComp3).first()
        rComp4 = listConditionOfSlope.objects.filter(id=resultComp4).first()
        rComp5 = listConditionOfSlope.objects.filter(id=resultComp5).first()
        # print(rComp1)

        qSetCondition = conditionOfSlope_M5
        result = qSetCondition.objects.create(
            slope_comp5_20_75=rComp1,
            slope_comp5_20_40=rComp3,
            slope_comp6_24_72=rComp2,
            slope_comp6_24_50=rComp4,
            slope_comp1_6_24=rComp5,
            ma=create
        )
        return result

    def setMAComp(self, vals, create):
        comp = compaireMA()
        m5_1 = Decimal(model_to_dict(create.m5)['close'])
        # ma_comp5_20_75
        resultComp1 = comp.comp3MA(vals[0], vals[5], vals[13])
        # ma_comp6_24_72
        resultComp2 = comp.comp3MA(vals[1], vals[6], vals[12])
        # ma_comp6_24_72
        resultComp3 = comp.comp3MA(vals[0], vals[5], vals[9])
        # ma_comp6_24_72
        resultComp4 = comp.comp3MA(vals[1], vals[6], vals[10])
        # ma_comp6_24_72
        resultComp5 = comp.comp3MA(m5_1, vals[1], vals[6])

        # 状態に関連するobject取得
        rComp1 = listConditionOfMA.objects.filter(id=resultComp1).first()
        rComp2 = listConditionOfMA.objects.filter(id=resultComp2).first()
        rComp3 = listConditionOfMA.objects.filter(id=resultComp3).first()
        rComp4 = listConditionOfMA.objects.filter(id=resultComp4).first()
        rComp5 = listConditionOfMA.objects.filter(id=resultComp5).first()

        qSetCondition = conditionOfMA_M5
        result = qSetCondition.objects.create(
            ma_comp5_20_75=rComp1,
            ma_comp5_20_40=rComp3,
            ma_comp6_24_72=rComp2,
            ma_comp6_24_50=rComp4,
            ma_comp1_6_24=rComp5,
            ma=create
        )
        return result

    def setConditionList(self, ma, macomp, slope, BBCondi):

        create = condition.objects.create(
            ma=ma,
            condition_of_slope_M5=slope,
            condition_of_ma_M5=macomp,
            condition_of_bb=BBCondi
        )

        return create
