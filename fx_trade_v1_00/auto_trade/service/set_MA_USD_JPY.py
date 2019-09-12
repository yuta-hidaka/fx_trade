from .get_MA_USD_JPY import getMA_USD_JPY
from ..models import M5_USD_JPY
from ..rest.serializers.set_candle_serialize import SetCandleSerializer


class setMA_USD_JPY:

    def setMA(self):

        qSet = M5_USD_JPY.objects.all()[:288].oderby(recorded_at)

        return dictM5
