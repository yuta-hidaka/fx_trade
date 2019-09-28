from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from decimal import *
from datetime import *
import numpy as np


class setBollingerBand_USD_JPY:
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
        todayMA = M50[idx]
        SMA = 0

        for M in M50:
            MClose = Decimal(M['mid']['c'])
            SMA += MClose
            # if latestDate > D['time']
        SMA = SMA / SMA_days

        SwD = 0
        listMA = []
        for M in M50:
            # SwD += (Decimal(M['mid']['c']) - SMA) ** Decimal(2)
            listMA.append(Decimal(M['mid']['c']))

        # SwD = ((SwD/SMA_days)**Decimal(0.5)) + SMA

        # 標準偏差の計算
        SD = np.std(listMA)
        SD1 = SD * Decimal(1)
        SD2 = SD * Decimal(2)
        SD3 = SD * Decimal(3)

        # 平均から本日分の終値の標準偏差を計算する。
        result, created = bollingerBand.objects.filter(
            recorded_at_utc=M50[idx]['time']).get_or_create(
            recorded_at_utc=M50[idx]['time'],
            sma_M50=SMA,
            abs_sigma_1=SD1,
            abs_sigma_2=SD2,

            abs_sigma_3=SD3,
        )

        return result, created
