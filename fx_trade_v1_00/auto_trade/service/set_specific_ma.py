from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import (
    M5_USD_JPY, MA_USD_JPY, SlopeM5_USD_JPY,
    conditionOfMA_M5, listConditionOfMA, listConditionOfSlope, condition, specificCandle, MA_Specific, tradeSettings
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

    def setMA(self, FXdata):
        comp = compaireMA()
        # 前回の設定を確認
        pastSettings = tradeSettings.objects.filter(id=2).first()

        settings = self.settings
        # 計算するデータ
        # 短期足
        shortLeg = settings.short_leg
        # 中期足
        middleLeg = settings.middle_leg
        # 長期足
        longLeg = settings.long_leg

        # 前回の短期足
        shortLegPast = pastSettings.short_leg
        # 前回の中期足
        middleLegPast = pastSettings.middle_leg
        # 前回の長期足
        longLegPast = pastSettings.long_leg

        sDef = False
        mDef = False
        lDef = False

        # 終値
        c = FXdata.close

        # 変数宣言
        vals = []
        listLeg = [shortLeg, middleLeg, longLeg]
        maList = []
        emaList = []

        is_first = False
        condiSlope = None

        maMaxNum = max(listLeg)
        maMax = list(specificCandle.objects.order_by(
            '-recorded_at_utc')[:maMaxNum].values())
        maCloseList = []

        for m in maMax:
            maCloseList.append(m['close'])

        # MA数の平均値を出力
        for maIndex in listLeg:
            idx = maIndex - 1
            # emaの計算
            if idx == 0:
                ma = maCloseList[idx]
            else:
                ma = np.mean(maCloseList[:idx])
            maList.append(ma)

            # 現在の最新MA一覧を取得する。
        try:
            leatestData = MA_Specific.objects.latest('created_at')
            pastShortEma = leatestData.ema_short
            pastMiddleEma = leatestData.ema_middle
            pastLongEma = leatestData.ema_long
            # print(FXdata)
        except Exception as e:
            pastShortEma = maList[0]
            pastMiddleEma = maList[1]
            pastLongEma = maList[2]
            is_first = True
            return print(e)
            print('MAの過去データがありません。')
            pass

        # 過去分の設定ファイルと違っていたらMAを過去のEMAとする
        if shortLeg != shortLegPast:
            pastShortEma = maList[0]
        if middleLeg != middleLegPast:
            pastMiddleEma = maList[1]
        if longLeg != longLegPast:
            pastLongEma = maList[2]

        # emaを計算
        shortEma = pastShortEma*(shortLeg-1)+(c*2)/(shortLeg+1)
        middleEma = pastMiddleEma*(shortLeg-1)+(c*2)/(shortLeg+1)
        longtEma = pastLongEma*(shortLeg-1)+(c*2)/(shortLeg+1)

        # MAの傾きを計算
        st = maList[0] - leatestData.ma_short
        md = maList[0] - leatestData.ma_middle
        lg = maList[0] - leatestData.ma_long

        qSet = MA_Specific
        # MA3つの位置を計算
        compMa = comp.comp3MA(maList[0], maList[1], maList[2])
        # MA3つの傾きを計算
        compSlope = comp.comp3MASlope(s=st, m=md, l=lg)

        print(compSlope)

        create = qSet.objects.create(
            m=FXdata,
            ma_short=maList[0],
            ma_middle=maList[1],
            ma_long=maList[2],

            ema_short=shortEma,
            ema_middle=middleEma,
            ema_long=longtEma,

            macd1=shortEma-middleEma,
            macd2=shortEma-longtEma,
            macd3=middleEma-longtEma,

            compMa=compMa,
            compSlope=int(compSlope)
        )

        pastSettings.short_leg = settings.short_leg
        pastSettings.middle_leg = settings.middle_leg
        pastSettings.long_leg = settings.long_leg

        pastSettings.save()

        return create

        # 値比較
        # result = self.sCondition.setMAComp(vals, create)

        # 現状を計算した情報を一テーブルに集約
        # return self.sCondition.setConditionList(create, result, condiSlope, BBCondi)
