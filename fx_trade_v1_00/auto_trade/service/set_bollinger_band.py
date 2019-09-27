from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY, bollingerBand
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from decimal import *
from datetime import *


class setBollingerBand_USD_JPY:
    # 20日　SMAを基準に標準偏差を算出していきます。
    def setBB(self):
        gMA = getMA_USD_JPY()
        created = False
        result = None
        # if gMA.get_5M_1()['candles']:
        if True:
            #     dictM5 = gMA.get_5M_1()['candles'][0]
            D20 = gMA.get_D_20()['candles']
            # D20 = D20.reverse()
            todayMA = D20[19]
            # D20 = sorted(D20,key=lambda parameter_list: expression)
            SMA = 0
            # SMA_days = len(D20)
            # latestDate = datetime.now()

            for D in D20:
                DClose = Decimal(D['mid']['c'])
                SMA += DClose
                # if latestDate > D['time']

            SMA = SMA / 20
            # 標準偏差の計算
            SD = ((
                SMA - Decimal(todayMA['mid']['c']))
                ** Decimal(2))**Decimal(0.5) + SMA
            SD1 = SD + Decimal(1)
            SD2 = SD + Decimal(2)
            SD3 = SD + Decimal(2)

            # 平均から本日分の終値の標準偏差を計算する。
            result, created = bollingerBand.objects.filter(
                recorded_at_utc=D20[19]['time']).get_or_create(
                recorded_at_utc=D20[19]['time'],
                sma_D20=SMA,
                abs_sigma_1=SD1,
                abs_sigma_2=SD2,
                abs_sigma_3=SD3,
            )

            # serial = SetCandleSerializer(data=dictM5)
            # if serial.is_valid():
            #     result, created = serial.create(serial.validated_data)
            #     print('setCandle_USD:is_valid')
            # else:
            #     print('setCandle_USD:is_not_valid')

        return result, created
