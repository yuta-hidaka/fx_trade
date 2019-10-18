from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand, conditionOfBB, listConditionOfBBTrande, batchLog, M5_USD_JPY, condition
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
        cond = condition.objects.all().order_by('-created_at')[:10]
        sig1 = (rs['abs_sigma_1'] * Decimal(1.5))
        sig2 = (rs['abs_sigma_2'] * Decimal(0.85))
        sig3 = (rs['abs_sigma_3'] * Decimal(0.9))

        bSig1 = (bbb['abs_sigma_1'] * Decimal(1.5))
        bSig2 = (bbb['abs_sigma_2'] * Decimal(0.85))
        bSig3 = (bbb['abs_sigma_3'] * Decimal(0.85))

        # sig1forEx = (rs['abs_sigma_1'])
        sig2forEx = (rs['abs_sigma_2'])

        # bSig1forEx = (bbb['abs_sigma_1'])
        bSig2forEx = (bbb['abs_sigma_2'])

        prevClose = Decimal(model_to_dict(condiPrev.ma.m5)['close'])

        nowClose = Decimal(nowMA.close)
        nowHigh = Decimal(nowMA.high)
        nowLow = Decimal(nowMA.low)

        JNowClose = Decimal(JustNowMA['candles'][0]['mid']['c'])
        JNowHigh = Decimal(JustNowMA['candles'][0]['mid']['h'])
        JNowLow = Decimal(JustNowMA['candles'][0]['mid']['l'])

        length = len(list(cond)) + 1
        data = 0
        slope = 0
        slopeDir = 0
        # is_squeeze=False
        is_plus = True
        is_peak = False
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

        sma = rs['sma_M50']
        bSma = bbb['sma_M50']

        # エクスパンション判断用
        sma2SigmaPlusEx = (
            sma + sig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusEx = (
            sma - sig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBeforEx = (
            bSma + bSig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBeforEx = (
            bSma - bSig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # エクスパンションピーク判断用
        sma3SigmaPlusExP = (
            sma + sig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusExP = (
            sma - sig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaPlusBeforExP = (
            bSma + bSig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusBeforExP = (
            bSma - bSig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 購買基準用
        sma2SigmaPlus = (
            sma + sig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinus = (
            sma - sig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBefor = (
            bSma + bSig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBefor = (
            bSma - bSig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 決済基準用のやつ
        sma1SigmaPlus = (
            sma + sig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinus = (
            sma - sig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaPlusBefor = (
            bSma + bSig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinusBefor = (
            bSma - bSig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        diff = (
            sma2SigmaPlusEx - sma2SigmaPlusBeforEx
        ).quantize(
            Decimal('0.0'),
            rounding=ROUND_HALF_UP
        )

        xClose = []
        yClose = []
        xClose.append(float(nowMA.close))
        for c in cond[:3]:
            xClose.append(float(c.ma.m5.close))

        try:
            xClose.reverse()
            x = np.arange(0, len(xClose))
            y = np.array(xClose)
            rs = np.polyfit(x, y, 1)
            slope = Decimal(rs[0]).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            slopeDir = np.sign(slope)

            text += str(rs['cv'])+' 変動係数<br>'
            text += str(rs[0])+' 傾き<br>'
            text += str(rs[1])+' 切片<br>'
            text += str(slopeDir)+' slopeDir<br>'

            pass
        except Exception as e:
            text += str(e)+' error<br>'
            pass

            # 持ち合い相場かトレンド相場かを判断
        aaaa = 0
        aaaa2 = 0
        aaaa3 = 0

        # text += str(nowMA.recorded_at_utc)+' 最新　<br>'
        # text += str(nowMA.close)+'　最新 close<br>'
        # text += str(sma)+'　最新 sma<br>'
        # text += str(nowMA.close - SMA)+'　最新 deff<br>'

        # yClose.append(Decimal(1))

        if nowMA.close - SMA == 0:
            data += 0
            aaaa += 1
        elif nowMA.close < SMA:
            data -= 1
            aaaa2 += 1
        elif nowMA.close > SMA:
            data += 1
            aaaa3 += 1

        for c in cond:
            if (c.ma.m5.close - c.condition_of_bb.bb.sma_M50) == 0:
                data += 0
                aaaa += 1
            elif c.ma.m5.close < c.condition_of_bb.bb.sma_M50:
                data -= 1
                aaaa2 += 1
            elif c.ma.m5.close > c.condition_of_bb.bb.sma_M50:
                data += 1
                aaaa3 += 1

        # for d in cBB:
        #     if (Decimal(m['mid']['c']) - d.bb.sma) == 0:
        #         data += 0
        #         aaaa += 1
        #     elif Decimal(m['mid']['c']) < SMA:
        #         data -= 1
        #         aaaa2 += 1
        #     elif Decimal(m['mid']['c']) > SMA:
        #         data += 1
        #         aaaa3 += 1

        # for m in MHalf:
        #     text += str(SMA) + ' : SMA<br>'
        #     text += str(m['mid']['c']) + ' : close<br>'
        #     try:
        #         text += str(m['time']) + ' : close<br>'
        #         pass
        #     except:
        #         pass
        #     text += str(SMA - Decimal(m['mid']['c'])) + ' : SMA - close<br>'

        #     if (Decimal(m['mid']['c']) - SMA) == 0:
        #         data += 0
        #         aaaa += 1
        #     elif Decimal(m['mid']['c']) < SMA:
        #         data -= 1
        #         aaaa2 += 1
        #     elif Decimal(m['mid']['c']) > SMA:
        #         data += 1
        #         aaaa3 += 1
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
        if np.absolute(ans) >= 80:
            is_trend = True
        else:
            is_trend = False

        if is_trend:
            if is_plus and slopeDir == 1:
                text += '＋トレンド<br>'
                # プラスのトレンド
                trandCondi = 1
            elif not is_plus and slopeDir == -1:
                text += '-トレンド<br>'
                # マイナスのトレンド
                trandCondi = 2
            elif slopeDir == 0:
                text += 'トレンドだけど傾きが真逆 一旦静観<br>'
                trandCondi = 4
            else:
                text += 'トレンドだけど傾きが真逆 一旦静観else<br>'
                trandCondi = 4
        else:
            # もみ合い相場
            text += '持ち合いトレンドcondition条件判定内<br>'
            trandCondi = 3

        if slopeDir == 0 and not is_trend:
            text += '傾き0でトレンドじゃない=スクイーズの可能性<br>'
            # 小数第二以上でプラスであればエクスパンション
            if diff != Decimal(0):
                is_expansion = True
                is_expansionByNum = True
                text += '価格差のエクスパンション<br>'

            # elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose and sma2SigmaPlus <= prevClose:
            # elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose:
            if sma2SigmaPlusEx <= nowClose and sma2SigmaPlusEx <= JNowClose:
                is_expansion = True
                is_expansionByStd = True
                is_topTouch = True
                text += '上にエクスパンション<br>'

            # elif sma2SigmaMinus >= nowClose and sma2SigmaMinus >= JNowClose and sma2SigmaMinus >= prevClose:
            if sma2SigmaMinusEx >= nowClose and sma2SigmaMinusEx >= JNowClose:
                is_expansion = True
                is_expansionByStd = True
                is_bottomTouch = True
                text += '下にエクスパンション<br>'
        else:
            text += '傾きが0ではなくトレンド<br>'

        # else:
        #     is_expansion = False

        # if nowClose
        # 持ち合い相場時の決済基準を判断
        text += 'nowHigh ' + str(nowHigh) + '<br>'
        text += 'JNowHigh ' + str(JNowHigh) + '<br>'
        text += 'nowLow ' + str(nowLow) + '<br>'
        text += 'JNowLow ' + str(JNowLow) + '<br>'
        text += 'SMA ' + str(SMA) + '<br>'
        text += 'sma2SigmaPlus ' + str(sma2SigmaPlus) + '<br>'
        text += 'sma2SigmaMinus ' + str(sma2SigmaMinus) + '<br>'
        text += 'sma1SigmaPlus ' + str(sma1SigmaPlus) + '<br>'
        text += 'sma1SigmaMinus ' + str(sma1SigmaMinus) + '<br>'
        text += 'JNowClose ' + str(JNowClose) + '<br>'
        text += 'nowClose ' + str(nowClose) + '<br>'

        if sma3SigmaPlusExP <= nowClose or sma3SigmaPlusExP <= nowClose:
            text += 'sigma3＋α closeが上に触りました<br>'
            is_topTouch = True
            is_peak = True
        elif sma3SigmaMinusExP >= nowClose or sma3SigmaMinusExP >= nowClose:
            text += 'sigma3＋α closeが下に触りました<br>'
            is_bottomTouch = True
            is_peak = True
        else:
            text += 'sigma3＋α どちらにも触れてません<br>'

        # if sma1SigmaPlus <= nowHigh or sma1SigmaPlus <= JNowHigh:
        if sma1SigmaPlus <= nowClose or sma1SigmaPlus <= nowClose:
            text += 'sigma1＋α 上に触りました<br>'
            is_longClose = True
        # elif sma1SigmaMinus >= nowLow or sma1SigmaMinus >= JNowLow:
        elif sma1SigmaMinus >= nowClose or sma1SigmaMinus >= nowClose:
            text += 'sigma1＋α 下に触りました<br>'
            is_shortClose = True
        else:
            text += 'sigma1＋α どちらにも触れてません<br>'

        # 持ち合い相場時の購買基準を判断
        # if sma2SigmaPlus <= nowHigh or sma2SigmaPlus <= JNowHigh:
        if sma2SigmaPlus <= nowClose or sma2SigmaPlus <= nowClose:
            is_shortIn = True
            is_topTouch = True
            text += 'sigma2＋α 上に触りました<br>'
        # elif sma2SigmaMinus >= nowLow or sma2SigmaMinus >= JNowLow:
        elif sma2SigmaMinus >= nowClose or sma2SigmaMinus >= nowClose:
            is_shortIn = False
            is_bottomTouch = True
            text += 'sigma2＋α 下に触りました<br>'
        else:
            text += 'sigma2＋α どちらにも触れてません<br>'

        create = conditionOfBB.objects.create(
            is_peak=is_peak,
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

        batchLog.objects.create(
            text=text
        )

        return create

        # 5MA*50　SMAを基準に標準偏差を算出していきます。

    def setBB(self, nowMA, condiPrev):
        gMA = getMA_USD_JPY()
        # is_squeeze = False
        created = False
        result = None
        # if gMA.get_5M_1()['candles']:
        #     dictM5 = gMA.get_5M_1()['candles'][0]
        # M50 = gMA.get_5M_50()['candles']
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
        # nowMA = M50[idx]

        listMA = []
        # listMAflt = []
        for M in M50:
            listMA.append(Decimal(M['mid']['c']))
            # listMAflt.append(float(M['mid']['c']))

        # text = ''
        # try:
        #     # listMAflt.reverse()
        #     x = np.arange(0, len(listMAflt))
        #     y = np.array(listMAflt)
        #     rs = np.polyfit(x, y, 1)
        #     slope = Decimal(rs[0]).quantize(
        #         Decimal('0.01'), rounding=ROUND_HALF_UP)
        #     slopeDir = np.sign(slope)
        #     text += str(rs[0])+' 傾き_SMA<br>'
        #     text += str(rs[1])+' 切片_SMA<br>'
        #     text += str(slopeDir)+' slopeDir_SMA<br>'

        #     pass
        # except Exception as e:
        #     text += str(e)+' error<br>'

        # if slopeDir == 0:
        #     is_squeeze = True
        #     text += ' スクイーズ中<br>'

        #     pass
        # batchLog.objects.create(
        #     text=text
        # )
        # SMA = np.average(listMA)
        SMA = np.mean(listMA)

        # 標準偏差の計算
        SD = np.std(listMA)
        # 変動係数の算出
        cv = SD / SMA
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
            cv=cv
        )

        resultBBCondi = self.setBBCondition(
            MHalf, SMA, nowMA, result, bbBefor, condiPrev
        )

        return resultBBCondi
