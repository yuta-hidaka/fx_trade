from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand, conditionOfBB, listConditionOfBBTrande, batchLog
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from decimal import *
from datetime import *
import numpy as np
from django.forms.models import model_to_dict


class setBollingerBand_USD_JPY:

    def setBBCondition(self, MHalf, SMA, nowMA, result, bbBefor, condiPrev):
        JustNowMA = getMA_USD_JPY().get_now()
        rs = model_to_dict(result)
        bbb = model_to_dict(bbBefor)

        rs['abs_sigma_2'] = (rs['abs_sigma_2']*Decimal(0.98)
                             ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        bbb['abs_sigma_2'] = (bbb['abs_sigma_2']*Decimal(0.98)
                              ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        rs['abs_sigma_2'] = (rs['abs_sigma_1']*Decimal(1.1)
                             ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        bbb['abs_sigma_2'] = (bbb['abs_sigma_1']*Decimal(1.1)
                              ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlus = (rs['sma_M50']+rs['abs_sigma_2']
                         ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma2SigmaMinus = (rs['sma_M50']-rs['abs_sigma_2']
                          ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma2SigmaPlusBefor = (bbb['sma_M50']+bbb['abs_sigma_2']
                              ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma2SigmaMinusBefor = (bbb['sma_M50']-bbb['abs_sigma_2']
                               ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaPlus = (rs['sma_M50']+rs['abs_sigma_1']
                         ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma1SigmaMinus = (rs['sma_M50']-rs['abs_sigma_1']
                          ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma1SigmaPlusBefor = (bbb['sma_M50']+bbb['abs_sigma_1']
                              ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        sma1SigmaMinusBefor = (bbb['sma_M50']-bbb['abs_sigma_1']
                               ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        prevClose = Decimal(model_to_dict(condiPrev.ma.m5)['close'])

        nowClose = Decimal(nowMA['mid']['c'])
        nowHigh = Decimal(nowMA['mid']['h'])
        nowLow = Decimal(nowMA['mid']['l'])

        JNowClose = Decimal(JustNowMA['candles'][0]['mid']['c'])
        JNowHigh = Decimal(JustNowMA['candles'][0]['mid']['h'])
        JNowLow = Decimal(JustNowMA['candles'][0]['mid']['l'])

        length = len(MHalf)
        data = 0
        is_plus = True
        is_trend = True
        is_shortIn = True
        is_topTouch = False
        is_bottomTouch = False
        is_expansion = False
        is_expansionByStd = False
        is_expansionByNum = False
        is_longClose = False
        is_shortClose = False
        trandCondi = 3
        listBB = listConditionOfBBTrande
        text = ''

        diff = (
            sma2SigmaPlus - sma2SigmaPlusBefor
        ).quantize(
            Decimal('0.0'),
            rounding=ROUND_HALF_UP
        )

        # 小数第二以上でプラスであればエクスパンション
        if diff != Decimal(0):
            is_expansion = True
            is_expansionByNum = True
            text += '価格差のエクスパンション<br>'

        # elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose and sma2SigmaPlus <= prevClose:
        elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose:
            is_expansion = True
            is_expansionByStd = True
            is_topTouch = True
            text += '上にエクスパンション<br>'

        # elif sma2SigmaMinus >= nowClose and sma2SigmaMinus >= JNowClose and sma2SigmaMinus >= prevClose:
        elif sma2SigmaMinus >= nowClose and sma2SigmaMinus >= JNowClose:
            is_expansion = True
            is_expansionByStd = True
            is_bottomTouch = True
            text += '下にエクスパンション<br>'

        else:
            is_expansion = False

        # if nowClose
        # 持ち合い相場時の決済基準を判断
            text += 'sma1SigmaPlus ' + str(sma1SigmaPlus) + '<br>'
            text += 'nowHigh ' + str(nowHigh) + '<br>'
            text += 'JNowHigh ' + str(JNowHigh) + '<br>'
            text += 'sma1SigmaMinus ' + str(sma1SigmaMinus) + '<br>'
            text += 'nowLow ' + str(nowLow) + '<br>'
            text += 'JNowLow ' + str(JNowLow) + '<br>'
            text += 'sma2SigmaPlus ' + str(sma2SigmaPlus) + '<br>'
            text += 'sma2SigmaMinus ' + str(sma2SigmaMinus) + '<br>'

            text += 'JNowClose ' + str(JNowClose) + '<br>'
            text += 'nowClose ' + str(nowClose) + '<br>'

        if sma1SigmaPlus <= nowHigh or sma1SigmaPlus <= JNowHigh:
            text += 'sigma1 上に触りました 持ち合い決済基準<br>'
            is_longClose = True
        elif sma1SigmaMinus >= nowLow or sma1SigmaMinus >= JNowLow:
            text += 'sigma1 下に触りました　持ち合い決済基準<br>'
            is_shortClose = True
        else:
            text += 'どちらにも触れてません　持ち合い決済基準<br>'

        # 持ち合い相場時の購買基準を判断
        if sma2SigmaPlus <= nowHigh or sma2SigmaPlus <= JNowHigh:
            is_shortIn = True
            is_topTouch = True
            text += 'sigma2 上に触りました<br>'
        elif sma2SigmaMinus >= nowLow or sma2SigmaMinus >= JNowLow:
            is_shortIn = False
            is_bottomTouch = True
            text += 'sigma2 下に触りました<br>'
        else:
            text += 'sigma2 どちらにも触れてません<br>'

        # 持ち合い相場かトレンド相場かを判断
        aaaa = 0
        aaaa2 = 0
        aaaa3 = 0

        for m in MHalf:
            if (Decimal(m['mid']['c']) - SMA) == 0:
                data += 0
                aaaa += 1
            elif Decimal(m['mid']['c']) < SMA:
                data -= 1
                aaaa2 += 1
            elif Decimal(m['mid']['c']) > SMA:
                data += 1
                aaaa3 += 1
        text += str(aaaa) + ' : 0のかず<br>'
        text += str(aaaa2) + ' : SMAより小さい<br>'
        text += str(aaaa3) + ' : SMAより大きい<br>'

        # SMAより上にあるか下にあるのが多いかを100分率で表示
        ans = (data / length)*100

        if np.sign(ans) == 1:
            is_plus = True
        else:
            is_plus = False

        # 90%より大きければトレンドが発生中
        # そうでなければ、もみ合い相場なので、ボリンジャーバンドでの売買を有効にしてもよい。
        text += str(np.absolute(ans)) + '% トレンド割合<br>'
        if np.absolute(ans) >= 90:
            is_trend = True
        else:
            is_trend = False

        if is_trend:
            if is_plus:
                text += '＋トレンド<br>'
                # プラスのトレンド
                trandCondi = 1
            else:
                text += '-トレンド<br>'
                # マイナスのトレンド
                trandCondi = 2
        else:
            # もみ合い相場
            text += 'もみ合いトレンドcondition条件判定内<br>'
            trandCondi = 3

        create = conditionOfBB.objects.create(
            is_expansion=is_expansion,
            is_topTouch=is_topTouch,
            is_bottomTouch=is_bottomTouch,
            is_expansionByStd=is_expansionByStd,
            is_expansionByNum=is_expansionByNum,
            is_shortClose=is_shortClose,
            is_longClose=is_longClose,
            is_shortIn=is_shortIn,
            bb_trande=listBB.objects.filter(id=trandCondi).first(),
            bb=result
        )

        text += 'diff<br>'
        text += str(diff) + '<br>'
        text += 'sma2SigmaPlus<br>'
        text += str(sma2SigmaPlus) + '<br>'
        text += 'sma2SigmaMinus<br>'
        text += str(sma2SigmaMinus) + '<br>'
        text += 'nowLow<br>'
        text += str(nowLow) + '<br>'
        text += 'JNowLow<br>'
        text += str(JNowLow) + '<br>'

        batchLog.objects.create(
            text=text
        )

        return create

        # 5MA*50　SMAを基準に標準偏差を算出していきます。

    def setBB(self, condiPrev):
        gMA = getMA_USD_JPY()
        created = False
        result = None
        # if gMA.get_5M_1()['candles']:
        #     dictM5 = gMA.get_5M_1()['candles'][0]
        M50 = gMA.get_5M_50()['candles']
        # M50 = M50.reverse()
        SMA_days = len(M50)
        idx = SMA_days - 1

        # 半分量をトレンド判定に使用する。
        stIdx = int(idx/2)
        # 偶数じゃなかったら偶数にする。
        if SMA_days % 2 != 0:
            stIdx += -1

        # 取得したMAの半分量→直近のトレンドを把握する。
        MHalf = M50[stIdx:idx]

        # 取得した最新のMA
        nowMA = M50[idx]

        listMA = []
        for M in M50:
            listMA.append(Decimal(M['mid']['c']))

        # SMA = np.average(listMA)
        SMA = np.mean(listMA)

        # 標準偏差の計算
        SD = np.std(listMA)
        SD1 = SD * Decimal(1)
        SD2 = SD * Decimal(2)
        SD3 = SD * Decimal(3)
        bbBefor = bollingerBand.objects.latest('created_at')

        # 平均から本日分の終値の標準偏差を計算する。
        result, created = bollingerBand.objects.filter(
            recorded_at_utc=M50[idx]['time']).get_or_create(
            recorded_at_utc=M50[idx]['time'],
            sma_M50=SMA,
            abs_sigma_1=SD1,
            abs_sigma_2=SD2,
            abs_sigma_3=SD3,
        )

        resultBBCondi = self.setBBCondition(
            MHalf, SMA, nowMA, result, bbBefor, condiPrev
        )

        return resultBBCondi
