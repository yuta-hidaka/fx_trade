from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer


class setCandle_USD:

    def setM5(self):
        gMA = getMA_USD_JPY()
        dictM5 = gMA.get_5M_1()['candles'][0]

        dictM5['record_time'] = dictM5.pop('time')
        dictM5['close'] = dictM5['mid']['c']
        dictM5['open'] = dictM5['mid']['o']
        dictM5['high'] = dictM5['mid']['h']
        dictM5['low'] = dictM5['mid']['l']

        serial = SetCandleSerializer(data=dictM5)
        if serial.is_valid():
            print('ok')
            serial.create(serial.validated_data)
        else:
            print('NG')

        # result, created = M5.objects.filter(
        #     report_time=dictM5['candles'][0]['time']
        # ).get_or_create(dictM5['candles'][0])

        return dictM5
