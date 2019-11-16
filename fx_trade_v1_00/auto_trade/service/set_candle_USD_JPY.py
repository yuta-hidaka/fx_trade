from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer
from datetime import datetime, timedelta, timezone


class setCandle_USD_JPY:

    def __init__(self):

        JST = timezone(timedelta(hours=+9), 'JST')
        dt_now = datetime.now(JST)
        self.text = "setCandle起動されました" + str(dt_now)

    def setM5(self):
        gMA = getMA_USD_JPY()
        created = False
        # デバッグ用(休日でデータが拾えない時用)
        result = None
        # result = M5_USD_JPY.objects.first()
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

    def setM1(self):
        gMA = getMA_USD_JPY()
        created = False
        # デバッグ用(休日でデータが拾えない時用)
        result = None
        # result = M5_USD_JPY.objects.first()
        rs = gMA.get_1M_num(1)
        if rs:

            rs = rs['candles'][0]
            rs['recorded_at_utc'] = rs.pop('time')
            rs['close'] = rs['mid']['c']
            rs['open'] = rs['mid']['o']
            rs['high'] = rs['mid']['h']
            rs['low'] = rs['mid']['l']

            serial = SetCandleSerializer(data=rs)
            if serial.is_valid():
                result, created = serial.create(serial.validated_data)
                # print('setCandle_USD:is_valid')
            else:
                print('setCandle_USD:is_not_valid')

        return result, created
