from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand, conditionOfBB, listConditionOfBBTrande
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from decimal import *
from datetime import *
import numpy as np
from django.forms.models import model_to_dict


class setBollingerBand_USD_JPY:

    def setBBCondition(self, MHalf, SMA, nowMA, result, bbBefor):
        rs = model_to_dict(result)
        bbb = model_to_dict(bbBefor)
        sma2SigmaPlus = rs['sma_M50']+rs['abs_sigma_2']
        sma2SigmaMinus = rs['sma_M50']-rs['abs_sigma_2']
        sma2SigmaPlusBefor = bbb['sma_M50']+bbb['abs_sigma_2']
        sma2SigmaMinusBefor = bbb['sma_M50']-bbb['abs_sigma_2']
        is_expansion = False

        diff = (
            sma2SigmaPlus - sma2SigmaPlusBefor
        ).quantize(
            Decimal('0.000'),
            rounding=ROUND_HALF_UP
        )

        # 小数第二以上でプラスであればエクスパンション
        if np.sign(diff) == 1:
            is_expansion = True

        nowClose = Decimal(nowMA['mid']['c'])
        nowHigh = Decimal(nowMA['mid']['h'])
        length = len(MHalf)
        data = 0
        is_plus = True
        is_trend = True
        is_shortIn = True
        is_topTouch = False
        is_bottomTouch = False
        trandCondi = 3
        listBB = listConditionOfBBTrande
        # if nowClose

        # 持ち合い相場時の購買基準を判断
        if sma2SigmaPlus <= nowHigh:
            is_shortIn = True
            is_topTouch = True
        elif sma2SigmaMinus >= nowHigh:
            is_shortIn = False
            is_bottomTouch = True
        else:
            is_shortIn = None

        # 持ち合い相場かトレンド相場かを判断
        print(SMA)
        print('SMA')
        dd1 = 0
        dd2 = 0
        dd3 = 0

        for m in MHalf:
            if (Decimal(m['mid']['c']) - SMA) == 0:
                data += 0
                dd1 += 1
            elif Decimal(m['mid']['c']) < SMA:
                data -= 1
                dd2 += 1

            elif Decimal(m['mid']['c']) > SMA:
                data += 1
                dd3 += 1

        print("上から0だった時、smaより小さかった時、smaより大きかった時の数量")
        print(dd1)
        print(dd2)
        print(dd3)

        # SMAより上にあるか下にあるのが多いかを100分率で表示
        ans = (data / length)*100
        f = np.sign(ans)
        print("np.sign(ans)")
        print(np.sign(ans))

        if np.sign(ans) == 1:
            is_plus = True
        else:
            is_plus = False

        # 80%より大きければトレンドが発生中
        # そうでなければ、もみ合い相場なので、ボリンジャーバンドでの売買を有効にしてもよい。
        if np.absolute(ans) >= 90:
            is_trend = True
        else:
            is_trend = False

        if is_trend:
            if is_plus:
                print('＋トレンド')
                # プラスのトレンド
                trandCondi = 1
            elif is_plus:
                print('-トレンド')
                # マイナスのトレンド
                trandCondi = 2
        else:
            # もみ合い相場
            print('もみ合いトレンドcondition条件判定内')
            trandCondi = 3

        create = conditionOfBB.objects.create(
            is_expansion=is_expansion,
            is_topTouch=is_topTouch,
            is_bottomTouch=is_bottomTouch,
            is_shortIn=is_shortIn,
            bb_trande=listBB.objects.filter(id=trandCondi).first(),
            bb=result
        )

        return create

        # 5MA*50　SMAを基準に標準偏差を算出していきます。

    def setBB(self):
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

        SMA = 0
        listMA = []
        for M in M50:
            MClose = Decimal(M['mid']['c'])
            listMA.append(Decimal(M['mid']['c']))
            SMA += MClose

        SMA = SMA / SMA_days

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

        resultBBCondi = self.setBBCondition(MHalf, SMA, nowMA, result, bbBefor)

        return resultBBCondi
