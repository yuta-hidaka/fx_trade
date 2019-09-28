from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer


class setCandle_USD_JPY:

    def setM5(self):
        gMA = getMA_USD_JPY()
        created = False
        # デバッグ用(休日でデータが拾えない時用)
        # result = M5_USD_JPY.objects.first()
        result = None
        if gMA.get_5M_1()['candles']:
            dictM5 = gMA.get_5M_1()['candles'][0]

            dictM5['recorded_at_utc'] = dictM5.pop('time')
            dictM5['close'] = dictM5['mid']['c']
            dictM5['open'] = dictM5['mid']['o']
            dictM5['high'] = dictM5['mid']['h']
            dictM5['low'] = dictM5['mid']['l']

            serial = SetCandleSerializer(data=dictM5)
            if serial.is_valid():
                result, created = serial.create(serial.validated_data)
                # print('setCandle_USD:is_valid')
            else:
                print('setCandle_USD:is_not_valid')

        return result, created
