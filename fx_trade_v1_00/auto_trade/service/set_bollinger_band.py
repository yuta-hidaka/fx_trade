from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand, conditionOfBB, listConditionOfBBTrande, batchLog, M5_USD_JPY, condition, tradeSettings
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from decimal import *
from datetime import *
import numpy as np
from django.forms.models import model_to_dict


class setBollingerBand_USD_JPY:

    def __init__(self):
        self.setting = tradeSettings.objects.filter(id=1).first()

    #     bb_count = models.IntegerField(default=50)
    # bb_cv_count = models.IntegerField(default=5)
    # bb_slope_dir_count = models.IntegerField(default=5)

    def setBBCondition(self, MHalf, nowMA, result, bbBefor, condiPrev):
        JustNowMA = getMA_USD_JPY().get_now()
        rs = model_to_dict(result)
        bbb = model_to_dict(bbBefor)
        cond = condition.objects.all().order_by(
            '-created_at')[:self.setting.bb_slope_dir_count]

        cond_2 = condition.objects.all().order_by(
            '-created_at')[:self.setting.bb_slope_dir_count]

        cv = rs['cv'].quantize(Decimal('0.00001'), rounding=ROUND_HALF_UP)
        text = ''

        try:
            text = str(rs['recorded_at_utc'])+'<br>'

            pass
        except:
            text = 'errrr'

            pass

        # sig_adj_settingsから取得
        sig1 = (rs['abs_sigma_1'] * self.setting.sig1_adj)
        sig2 = (rs['abs_sigma_2'] * self.setting.sig2_adj)
        sig3 = (rs['abs_sigma_3'] * self.setting.sig3_adj)

        sig1_2 = (rs['abs_sigma_1_2'] * self.setting.sig1_adj)
        sig2_2 = (rs['abs_sigma_2_2'] * self.setting.sig2_adj)
        sig3_2 = (rs['abs_sigma_3_2'] * self.setting.sig3_adj)

        bSig1 = (bbb['abs_sigma_1'] * self.setting.sig1_adj)
        bSig2 = (bbb['abs_sigma_2'] * self.setting.sig2_adj)
        bSig3 = (bbb['abs_sigma_3'] * self.setting.sig3_adj)

        bSig1_2 = (bbb['abs_sigma_1_2'] * self.setting.sig1_adj)
        bSig2_2 = (bbb['abs_sigma_2_2'] * self.setting.sig2_adj)
        bSig3_2 = (bbb['abs_sigma_3_2'] * self.setting.sig3_adj)

        # エクスパンション判定用
        sig2forEx = (rs['abs_sigma_2'])
        sig2forEx_2 = (rs['abs_sigma_2_2'])

        bSig2forEx = (bbb['abs_sigma_2'])
        bSig2forEx_2 = (bbb['abs_sigma_2_2'])

        prevClose = Decimal(model_to_dict(condiPrev.ma.m5)['close'])
        bfClose = condiPrev.ma.m5.close
        bfHigh = condiPrev.ma.m5.high
        bfLow = condiPrev.ma.m5.low

        nowClose = Decimal(nowMA.close)
        nowHigh = Decimal(nowMA.high)
        nowLow = Decimal(nowMA.low)

        JNowClose = Decimal(JustNowMA['candles'][0]['mid']['c'])
        JNowHigh = Decimal(JustNowMA['candles'][0]['mid']['h'])
        JNowLow = Decimal(JustNowMA['candles'][0]['mid']['l'])

        length = len(list(cond)) + 1
        data = 0
        data_2 = 0
        slope_cv = 0
        slope = 0
        slope_2 = 0
        slopeDir = 0
        slopeDir_2 = 0
        # is_squeeze=False
        is_plus = True
        is_peak = False
        is_trend = True
        is_shortIn = True
        is_longIn = False
        is_topTouch = False
        is_bottomTouch = False
        is_expansion = False
        is_expansionByStd = False
        is_expansionByNum = False
        is_longClose = False
        is_shortClose = False

        trandCondi = 3
        listBB = listConditionOfBBTrande

        sma = rs['sma']
        sma_2 = rs['sma_2']
        bSma = bbb['sma']
        bSma_2 = bbb['sma_2']

        # エクスパンション判断用
        sma2SigmaPlusEx = (
            sma + sig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusEx = (
            sma - sig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBeforEx = (
            bSma + bSig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBeforEx = (
            bSma - bSig2forEx).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # エクスパンション判断用　上位足のチェック用
        sma2SigmaPlusEx_2 = (
            sma_2 + sig2forEx_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusEx_2 = (
            sma_2 - sig2forEx_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBeforEx_2 = (
            bSma_2 + bSig2forEx_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBeforEx_2 = (
            bSma_2 - bSig2forEx_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # エクスパンションピーク判断用
        sma3SigmaPlusExP = (
            sma + sig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusExP = (
            sma - sig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaPlusBeforExP = (
            bSma + bSig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusBeforExP = (
            bSma - bSig3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # エクスパンションピーク判断用
        sma3SigmaPlusExP_2 = (
            sma_2 + sig3_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusExP_2 = (
            sma_2 - sig3_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaPlusBeforExP_2 = (
            bSma_2 + bSig3_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma3SigmaMinusBeforExP_2 = (
            bSma_2 - bSig3_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 購買基準用
        sma2SigmaPlus = (
            sma + sig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinus = (
            sma - sig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBefor = (
            bSma + bSig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBefor = (
            bSma - bSig2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 購買基準用
        sma2SigmaPlus_2 = (
            sma_2 + sig2_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinus_2 = (
            sma_2 - sig2_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaPlusBefor_2 = (
            bSma_2 + bSig2_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma2SigmaMinusBefor_2 = (
            bSma_2 - bSig2_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 決済基準用のやつ
        sma1SigmaPlus = (
            sma + sig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinus = (
            sma - sig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaPlusBefor = (
            bSma + bSig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinusBefor = (
            bSma - bSig1).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        # 決済基準用のやつ
        sma1SigmaPlus_2 = (
            sma_2 + sig1_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinus_2 = (
            sma_2 - sig1_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaPlusBefor_2 = (
            bSma_2 + bSig1_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        sma1SigmaMinusBefor = (
            bSma_2 - bSig1_2).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        diff = (
            sma2SigmaPlusEx - sma2SigmaPlusBeforEx
        ).quantize(
            Decimal('0.0'),
            rounding=ROUND_HALF_UP
        )
        diff_2 = (
            sma2SigmaPlusEx - sma2SigmaPlusBeforEx
        ).quantize(
            Decimal('0.0'),
            rounding=ROUND_HALF_UP
        )

        xClose = []
        xClose_2 = []
        xClose.append(float(nowMA.close))

        for c in cond[:self.setting.bb_cv_count]:
            xClose.append(float(c.ma.m5.close))

        try:
            xClose.reverse()
            x = np.arange(0, len(xClose))
            y = np.array(xClose)
            rs = np.polyfit(x, y, 1)
            dcml = str(rs[0])
            slope_cv = Decimal(dcml).quantize(
                Decimal('0.01'), rounding=ROUND_DOWN)
            slopeDir = np.sign(slope_cv)

# -----------------------------------------------------------------------
            slope_01 = Decimal(dcml).quantize(
                Decimal('0.1'), rounding=ROUND_DOWN)
            slope_001 = Decimal(dcml).quantize(
                Decimal('0.01'), rounding=ROUND_DOWN)

            slopeDir_01 = np.sign(slope_01)
            slopeDir_001 = np.sign(slope_001)
# -----------------------------------------------------------------------

            s001 = Decimal('0.01039999999999003').quantize(
                Decimal('0.01'), rounding=ROUND_DOWN)
            text += ' test 0.01039999999999003を丸めた<br>'
            text += str(s001)+' 傾き<br>'

            text += str(rs[0])+' 傾き<br>'
            text += str(rs[1])+' 切片<br>'
            text += str(slope_001)+' slopeDir 0.01で丸めたバージョン<br>'
            text += str(slopeDir_001)+' slopeDir 0.01で丸めたバージョン<br>'
            text += str(slope_01)+' slopeDir 0.1で丸めたバージョン<br>'
            text += str(slopeDir_01)+' slopeDir 0.1で丸めたバージョン<br>'
            pass
        except Exception as e:
            text += str(e)+' error<br>'
            pass

            # 持ち合い相場かトレンド相場かを判断
        aaaa = 0
        aaaa2 = 0
        aaaa3 = 0

        aaaa_2 = 0
        aaaa2_2 = 0
        aaaa3_2 = 0
        # １つ目
        if nowMA.close - sma == 0:
            data += 0
            aaaa += 1
        elif nowMA.close < sma:
            data -= 1
            aaaa2 += 1
        elif nowMA.close > sma:
            data += 1
            aaaa3 += 1

        # ２つ目
        if nowMA.close - sma_2 == 0:
            data_2 += 0
            aaaa_2 += 1
        elif nowMA.close < sma_2:
            data_2 -= 1
            aaaa2_2 += 1
        elif nowMA.close > sma_2:
            data_2 += 1
            aaaa3_2 += 1

        xClose = []
        for c in cond:
            xClose.append(float(c.ma.m5.close))
            if (c.ma.m5.close - c.condition_of_bb.bb.sma) == 0:
                data += 0
                aaaa += 1
            elif c.ma.m5.close < c.condition_of_bb.bb.sma:
                data -= 1
                aaaa2 += 1
            elif c.ma.m5.close > c.condition_of_bb.bb.sma:
                data += 1
                aaaa3 += 1

            # ２つ目
            if nowMA.close - c.condition_of_bb.bb.sma_2 == 0:
                data_2 += 0
                aaaa_2 += 1
            elif nowMA.close < c.condition_of_bb.bb.sma_2:
                data_2 -= 1
                aaaa2_2 += 1
            elif nowMA.close > c.condition_of_bb.bb.sma_2:
                data_2 += 1
                aaaa3_2 += 1

        xClose.reverse()
        x = np.arange(0, len(xClose))
        y = np.array(xClose)
        rs = np.polyfit(x, y, 1)
        slope = Decimal(rs[0]).quantize(
            Decimal('0.01'), rounding=ROUND_UP)
        slopeDir2 = np.sign(slope)

        text += str(aaaa) + ' : 0のかず<br>'
        text += str(aaaa2) + ' : SMAより小さい<br>'
        text += str(aaaa3) + ' : SMAより大きい<br>'
        text += str(aaaa_2) + ' : 0のかず②<br>'
        text += str(aaaa2_2) + ' : SMAより小さい②<br>'
        text += str(aaaa3_2) + ' : SMAより大きい②<br>'

        # SMAより上にあるか下にあるのが多いかを100分率で表示
        ans = (data / length)*100
        ans_2 = (data_2 / length)*100

        if np.sign(ans) == 1 or np.sign(ans_2) == 1:
            is_plus = True
        else:
            is_plus = False

        # 90%より大きければトレンドが発生中
        # そうでなければ、もみ合い相場なので、ボリンジャーバンドでの売買を有効にしてもよい。
        text += str(np.absolute(ans)) + '% トレンド割合<br>'

        text += str(aaaa) + ' : 0のかず<br>'
        text += str(aaaa2) + ' : SMAより小さい<br>'
        text += str(aaaa3) + ' : SMAより大きい<br>'

        text += '----------------------------------------------<br>'
        text += str(aaaa_2) + ' : 0のかず<br>'
        text += str(aaaa2_2) + ' : SMAより小さい<br>'
        text += str(aaaa3_2) + ' : SMAより大きい<br>'
        # if slopeDir == 0 and not is_trend:
        # text += '傾き0でトレンドじゃない=スクイーズの可能性<br>'
        # 小数第二以上でプラスであればエクスパンション
        if slopeDir != 0:
            if diff != Decimal(0):
                is_expansion = True
                is_expansionByNum = True
                text += '価格差のエクスパンション<br>'
            elif diff_2 != Decimal(0):
                is_expansion = True
                is_expansionByNum = True
                text += '価格差のエクスパンション②<br>'
            # elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose and sma2SigmaPlus <= prevClose:
            # elif sma2SigmaPlus <= nowClose and sma2SigmaPlus <= JNowClose:
            # if sma2SigmaPlusEx <= nowClose and sma2SigmaPlusEx <= JNowClose:
            if sma2SigmaPlusEx <= nowClose and sma2SigmaPlusEx_2 <= nowClose:
                is_expansion = True
                is_expansionByStd = True
                is_topTouch = True
                text += '上にエクスパンション<br>'
            # elif sma2SigmaPlusEx_2 <= nowClose:
            #     is_expansion = True
            #     is_expansionByStd = True
            #     is_topTouch = True
            #     text += '上にエクスパンション②<br>'
            # elif sma2SigmaMinus >= nowClose and sma2SigmaMinus >= JNowClose and sma2SigmaMinus >= prevClose:
            # if sma2SigmaMinusEx >= nowClose and sma2SigmaMinusEx >= JNowClose:
            if sma2SigmaMinusEx >= nowClose and sma2SigmaMinusEx_2 >= nowClose:
                is_expansion = True
                is_expansionByStd = True
                is_bottomTouch = True
                text += '下にエクスパンション<br>'
            # elif sma2SigmaMinusEx_2 >= nowClose:
            #     is_expansion = True
            #     is_expansionByStd = True
            #     is_bottomTouch = True
            #     text += '下にエクスパンション②<br>'
            # else:
            #     is_expansion = False

        if not is_expansion:
            trendRatio = 90
            if np.absolute(ans) >= trendRatio:
                # if np.absolute(ans) >= trendRatio or np.absolute(ans_2) >= trendRatio:
                is_trend = True
            else:
                is_trend = False

            if is_trend:
                if is_plus and slopeDir == 1:
                    text += '＋トレンド<br>'
                    # プラスのトレンド
                    trandCondi = 1
                    is_longIn = True
                elif not is_plus and slopeDir == -1:
                    text += '-トレンド<br>'
                    # マイナスのトレンド
                    trandCondi = 2
                    is_shortIn = True
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

        # if nowClose
        # 持ち合い相場時の決済基準を判断
        text += 'is_trend ' + str(is_trend) + '<br>'
        text += 'nowHigh ' + str(nowHigh) + '<br>'
        text += 'JNowHigh ' + str(JNowHigh) + '<br>'
        text += 'nowLow ' + str(nowLow) + '<br>'
        text += 'JNowLow ' + str(JNowLow) + '<br>'
        text += 'JNowClose ' + str(JNowClose) + '<br>'
        text += 'nowClose ' + str(nowClose) + '<br>'
        text += 'bfClose ' + str(bfClose) + '<br>'
        text += 'SMA ' + str(sma) + '<br>'
        text += 'sma1SigmaPlus ' + str(sma1SigmaPlus) + '<br>'
        text += 'sma2SigmaPlus ' + str(sma2SigmaPlus) + '<br>'
        text += 'sma1SigmaMinus ' + str(sma1SigmaMinus) + '<br>'
        text += 'sma2SigmaMinus ' + str(sma2SigmaMinus) + '<br>'
        text += 'SMA2 ' + str(sma_2) + '<br>'
        text += 'sma1SigmaPlus_2 ' + str(sma1SigmaPlus_2) + '<br>'
        text += 'sma2SigmaPlus_2 ' + str(sma2SigmaPlus_2) + '<br>'
        text += 'sma1SigmaMinus_2 ' + str(sma1SigmaMinus_2) + '<br>'
        text += 'sma2SigmaMinus_2 ' + str(sma2SigmaMinus_2) + '<br>'
        # peak  判定
        if sma3SigmaPlusExP >= nowClose and sma3SigmaPlusBeforExP <= bfClose:
            # if sma3SigmaPlusExP <= nowClose or sma3SigmaPlusExP <= nowClose:
            # if sma2SigmaMinusEx <= nowClose and sma2SigmaMinusEx <= JNowClose:
            text += 'sigma3＋α closeが上に触りました<br>'
            is_topTouch = True
            is_peak = True
        elif sma3SigmaMinusExP >= nowClose and sma3SigmaMinusExP >= bfClose:
            text += 'sigma3＋α closeが下に触りました<br>'
            is_bottomTouch = True
            is_peak = True
        else:
            text += 'sigma3＋α どちらにも触れてません<br>'

            if sma3SigmaPlusExP_2 >= nowClose and sma3SigmaPlusBeforExP_2 <= bfClose:
                    # if sma3SigmaPlusExP <= nowClose or sma3SigmaPlusExP <= nowClose:
                    # if sma2SigmaMinusEx <= nowClose and sma2SigmaMinusEx <= JNowClose:
                text += 'sigma3＋α closeが上に触りました②<br>'
                is_topTouch = True
                is_peak = True
            elif sma3SigmaMinusExP_2 >= nowClose and sma3SigmaMinusExP_2 >= bfClose:
                text += 'sigma3＋α closeが下に触りました②<br>'
                is_bottomTouch = True
                is_peak = True
            else:
                text += 'sigma3＋α どちらにも触れてません②<br>'

        if not is_trend:
            # 売却判定
            # if sma1SigmaPlus <= nowHigh or sma1SigmaPlus <= JNowHigh:
            if sma1SigmaPlus <= nowClose or sma1SigmaPlus <= nowClose:
                # if sma1SigmaPlus <= nowClose or sma1SigmaPlus <= nowClose and slopeDir2 == -1:
                text += 'sigma1＋α 上に触りました<br>'
                is_longClose = True
            # elif sma1SigmaMinus >= nowLow or sma1SigmaMinus >= JNowLow:
            elif sma1SigmaMinus >= nowClose or sma1SigmaMinus >= nowClose:
                # elif sma1SigmaMinus >= nowClose or sma1SigmaMinus >= nowClose and slopeDir2 == 1:
                text += 'sigma1＋α 下に触りました<br>'
                is_shortClose = True
            else:
                text += 'sigma1＋α どちらにも触れてません<br>'

                # 売却判定②
                # if sma1SigmaPlus <= nowHigh or sma1SigmaPlus <= JNowHigh:
                if sma1SigmaPlus_2 <= nowClose or sma1SigmaPlus_2 <= nowClose:
                    # if sma1SigmaPlus <= nowClose or sma1SigmaPlus <= nowClose and slopeDir2 == -1:
                    text += 'sigma1＋α 上に触りました②<br>'
                    is_longClose = True
                # elif sma1SigmaMinus >= nowLow or sma1SigmaMinus >= JNowLow:
                elif sma1SigmaMinus_2 >= nowClose or sma1SigmaMinus_2 >= nowClose:
                    # elif sma1SigmaMinus >= nowClose or sma1SigmaMinus >= nowClose and slopeDir2 == 1:
                    text += 'sigma1＋α 下に触りました②<br>'
                    is_shortClose = True
                else:
                    text += 'sigma1＋α どちらにも触れてません②<br>'

            # 持ち合い相場時の購買基準を判断
            if sma2SigmaPlus <= nowHigh or sma2SigmaPlus <= JNowHigh:
                # if sma2SigmaPlus <= nowClose or sma2SigmaPlus <= nowClose:
                # is_longClose = True
                is_shortIn = True
                is_topTouch = True
                text += 'sigma2＋α 上に高値のみ触りました high not close<br>'
            elif sma2SigmaMinus >= nowLow or sma2SigmaMinus >= JNowLow:
                # elif sma2SigmaMinus >= nowClose or sma2SigmaMinus >= nowClose:
                # is_shortClose = True
                # is_shortIn = False
                is_longIn = True
                is_bottomTouch = True
                text += 'sigma2＋α 下に底値のみ触りましたlow not close<br>'
            else:
                text += 'sigma2＋α どちらにも触れてません<br>'
                # 持ち合い相場時の購買基準を判断
                if sma2SigmaPlus_2 <= nowHigh or sma2SigmaPlus_2 <= JNowHigh:
                    # if sma2SigmaPlus <= nowClose or sma2SigmaPlus <= nowClose:
                    # is_longClose = True
                    is_shortIn = True
                    is_topTouch = True
                    text += 'sigma2＋α 上に高値のみ触りました②high not close<br>'
                elif sma2SigmaMinus_2 >= nowLow or sma2SigmaMinus_2 >= JNowLow:
                    # elif sma2SigmaMinus >= nowClose or sma2SigmaMinus >= nowClose:
                    # is_shortClose = True
                    # is_shortIn = False
                    is_longIn = True
                    is_bottomTouch = True
                    text += 'sigma2＋α 下に底値のみ触りました②low not close<br>'
                else:
                    text += 'sigma2＋α どちらにも触れてません②<br>'

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
            is_longIn=is_longIn,
            bb_trande=listBB.objects.filter(id=trandCondi).first(),
            bb=result,
            slope_001=slopeDir_001,
            slope_01=slopeDir_01
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

        # mas = gMA.get_5M_num(self.setting.bb_count)['candles']
        mas = gMA.get_1M_num(num = self.setting.bb_count)['candles']
        text = ''
        text = str(self.setting.bb_count)

        # M50 = M50.reverse()
        SMA_days = len(mas)
        idx = SMA_days - 1

        # 半分量をトレンド判定に使用する。
        stIdx = int(idx/2)
        # 偶数じゃなかったら偶数にする。
        if SMA_days % 2 != 0:
            stIdx += -1

        # 取得したMAの半分量→直近のトレンドを把握する。
        MHalf = mas[stIdx:idx]

        # 取得した最新のMA
        # nowMA = M50[idx]

        listMA = []
        # listMAflt = []
        for M in mas:
            listMA.append(Decimal(M['mid']['c']))
            text += 'days ' + str(M['time']) + '<br>'
        # listMAflt.append(float(M['mid']['c']))

        SMA = np.mean(listMA)
        # 標準偏差の計算
        SD = np.std(listMA)
        # 変動係数の算出
        cv = SD / SMA
        SD1 = SD * Decimal('1')
        SD2 = SD * Decimal('2')
        SD3 = SD * Decimal('3')
        text += 'SMA_days ' + str(SMA_days) + '<br>'
        text += 'SMA ' + str(SMA) + '<br>'
        text += 'SD1 ' + str(SMA + SD1) + '<br>'
        text += 'SD2 ' + str(SMA + SD2) + '<br>'
        text += 'SD3 ' + str(SMA + SD3) + '<br>'

        # mas2 = gMA.get_5M_num(self.setting.bb_count_2)['candles']
        mas2 = gMA.get_1M_num(self.setting.bb_count_2)['candles']

        listMA2 = []
        # listMAflt = []
        for M in mas2:
            listMA2.append(Decimal(M['mid']['c']))
            # listMAflt.append(float(M['mid']['c']))
        SMA2 = np.mean(listMA2)
        # 標準偏差の計算
        SD_2 = np.std(listMA2)
        # 変動係数の算出
        cv2 = SD_2 / SMA2
        SD1_2 = SD_2 * Decimal('1')
        SD2_2 = SD_2 * Decimal('2')
        SD3_2 = SD_2 * Decimal('3')

        text += 'SMA2 ' + str(SMA2) + '<br>'
        text += 'SD1_2 ' + str(SMA2 + SD1_2) + '<br>'
        text += 'SD2_2 ' + str(SMA2 + SD2_2) + '<br>'
        text += 'SD3_2 ' + str(SMA2 + SD3_2) + '<br>'

        bbBefor = bollingerBand.objects.latest('created_at')

        # 平均から本日分の終値の標準偏差を計算する。
        result, created = bollingerBand.objects.filter(
            recorded_at_utc=mas[idx]['time']).get_or_create(
            recorded_at_utc=mas[idx]['time'],
            sma=SMA,
            abs_sigma_1=SD1,
            abs_sigma_2=SD2,
            abs_sigma_3=SD3,
            sma_2=SMA2,
            abs_sigma_1_2=SD1_2,
            abs_sigma_2_2=SD2_2,
            abs_sigma_3_2=SD3_2,
            cv=cv
        )
        batchLog.objects.create(
            text=text
        )

        resultBBCondi = self.setBBCondition(
            MHalf, nowMA, result, bbBefor, condiPrev
        )

        return resultBBCondi
