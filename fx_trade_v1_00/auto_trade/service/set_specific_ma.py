from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import (
    M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY,
    conditionOfMA_M5, listConditionOfMA, listConditionOfSlope, condition, specificCandle, MA_Specific
)
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from django.db.models import Avg
from decimal import *
from django.forms.models import model_to_dict
from ..calculate.compare_ma import compaireMA
from django.core.exceptions import ObjectDoesNotExist
from .set_condition import setCondition
import numpy as np


class setSpecificMA:

    def __init__(self):
        self.sCondition = setCondition()
        self.settings = None

    def setMASlope(self, preveousData, leatestData):

        ListMa = [5, 6, 10, 12, 15, 20, 24, 30, 36,
                  40, 50, 70, 72, 75, 140, 144, 150, 288]
        vals = []
        comp = compaireMA()

        ld = model_to_dict(leatestData)
        pd = model_to_dict(preveousData)

        for ma in ListMa:
            key = 'm5_ma' + str(ma)
            data = Decimal(
                ld[key])-(pd[key]
                          ).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            # ).quantize(Decimal('0.01'), rounding = ROUND_HALF_UP)
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

    def setMA(self, FXdata):
        settings = self.settings
        # 計算するデータ
        # 短期足
        shortLeg = settings.short_leg
        # 中期足
        middleLeg = settings.middle_leg
        # 長期足
        longLeg = settings.long_leg

        # 変数宣言
        vals = []
        listLeg = [shortLeg, middleLeg, longLeg]
        maList = []
        emaList = []

        is_first = False
        condiSlope = None

        # 現在の最新MA一覧を取得する。
        try:
            leatestData = specificCandle.objects.latest('created_at')
            # print(FXdata)
        except ObjectDoesNotExist:
            is_first = True
            print('MAの過去データがありません。')
            pass

        maMaxNum = max(listLeg)
        maMax = list(specificCandle.objects.order_by(
            '-recorded_at_utc')[:maMaxNum].values())
        maCloseList = []

        for m in maMax:
            maCloseList.append(m['close'])

        # MA数の平均値を出力
        for ma in listLeg:
            # if ma-1 == 0:
            e = maCloseList[:1][0] * 2

            # emaの計算
            if ma == 1:
                ema = e/2
            else:
                pstE = np.mean(maCloseList[1:ma])
                ema = (e+Decimal(pstE))/(ma + 1)

            emaList.append(ema)

            # maの計算
            maList.append(np.mean(maCloseList[:ma]))

        qSet = MA_Specific
        create = qSet.objects.create(
            m=FXdata,
            ma_short=listLeg[0],
            ma_middle=listLeg[1],
            ma_long=listLeg[2],
            ema_short=emaList[0],
            ema_middle=emaList[1],
            ema_long=emaList[2],
        )

        return create

        # 値比較
        # result = self.sCondition.setMAComp(vals, create)

        # 現状を計算した情報を一テーブルに集約
        # return self.sCondition.setConditionList(create, result, condiSlope, BBCondi)
