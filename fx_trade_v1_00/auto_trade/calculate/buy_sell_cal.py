from ..models import MA_USD_JPY, orderStatus
from django.forms.models import model_to_dict
from ..service.get_MA_USD_JPY import getMA_USD_JPY
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
from fx_trade_v1_00.lib.access_token import FxInfo
from fx_trade_v1_00.lib.order import orderFx
import json
from decimal import *

# MAを比較する
# 5分足 5本、20本、75本で比較する。

'''受け取った短期、中期、長期のMAを比較してどの状態にいるのかを判断します・'''


class BuySellCal():
    def __init__(self):
        self.fx = FxInfo()
        self.order = orderFx()

    def BuySellCheck(self, condNow, condiPrev):

        # 口座のすべてのポジションをリストとして取得
        r = positions.PositionList(accountID=self.fx.accountID)
        api = self.fx.api
        res = api.request(r)
        pos = res['positions'][0]
        # オーダーステータスを取得する。
        try:
            orderLongNum = len(pos['long']['tradeIDs'])
        except:
            orderLongNum = 0

        try:
            orderShortNum = len(pos['short']['tradeIDs'])
        except:
            orderShortNum = 0

        units = 2500
        # print(json.dumps(res, indent=2))
        print('BuySellCheck')
        getNowRate = getMA_USD_JPY()
        # print(model_to_dict(condition))
        # ma_comp6_24_50＿＿＿＿＿＿＿＿＿2019/09/23現在
        # t = condition.select_related()
        # 前回のMAが6or1で今が1で現状がすべて正だったらlong　in
        # 現状が2になったらlongの解体
        # 前回が3or4かつ、現在が4の状態ですべての傾きが負でshort
        # 5の状態であれば売りの手じまい
        # 　現在4パターン
        # longで二つ、shortで二つ
        # 購買基準　現在の為替を取得する。そこからlongは+0.02%乗じる、shortは-0.02%でorder
        # 損切の設定はlongは-0.05%乗じる、shortは+0.05%
        # 売買時にどの程度購入する？所有金額の半分をぶち込む
        # 売買時は問答無用で清算
        # longとshotにはひとつづつしかポジションを持たない。
        # 購買する際にはポジションを所有しているかチェック

        # 傾きの状態は前回と比較する必要がない。

        M5_1 = getNowRate.get_5M_now()
        # M5_1 = getNowRate.get_5M_1()

        # 現在の為替情報をその5分10分前の為替の終値を取得する。
        M5_1_close = Decimal(M5_1['candles'][0]['mid']['c'])
        M5_1_closeNow = model_to_dict(condNow.ma.m5)['close']
        M5_1_closePrev = model_to_dict(condiPrev.ma.m5)['close']

        # 市場が閉じていたら計算等は行わない
        if not len(M5_1['candles']) == 0:
            # self.order.orderCreate()

            print('----------------------------------------------------------------------------------------------------')

            long_in = (
                M5_1_close + M5_1_close*Decimal(0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            long_limit = (
                M5_1_close + M5_1_close*Decimal(-0.0005)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            short_in = (
                M5_1_close + M5_1_close*Decimal(-0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            short_limit = (
                M5_1_close + M5_1_close*Decimal(0.0005)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            maPrev = model_to_dict(
                condiPrev.condition_of_ma_M5
            )['ma_comp1_6_24']

            maNow = model_to_dict(
                condNow.condition_of_ma_M5
            )['ma_comp1_6_24']

            slopePrev = model_to_dict(
                condiPrev.condition_of_slope_M5
            )['slope_comp1_6_24']

            slopeNow = model_to_dict(
                condNow.condition_of_slope_M5
            )['slope_comp1_6_24']

            # longのタイミング all slope is positive and before MA is 6or1 and now 1
            if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
                if not orderLongNum >= 2:
                    print("long in 以下short order数")
                    print(orderLongNum)
                    self.order.price = str(long_in)
                    self.order.stopLoss = str(long_limit)
                    self.order.units = str(units)
                    self.order.orderCreate()
                else:
                    print("long in　but position is too many")

                    # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
            elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                if not orderShortNum >= 2:
                    print("short in　以下short order数")
                    self.order.price = str(short_in)
                    self.order.stopLoss = str(short_limit)
                    self.order.units = str(units*-1)
                    self.order.orderCreate()
                else:
                    print("short in　but position is too many")

                    # long closeのタイミング if MA is 2 it have to close
            elif maNow == 2:
                print("long out")
                self.order.oderCloseAllLong()

            # short　closeのタイミング if MA is 5 it have to close
            elif maNow == 5:
                print("short out")
                self.order.oderCloseAllShort()

            # long　closeのタイミング。過去10分間と現状が上がり続けていたら閉じる
            elif M5_1_close > M5_1_closeNow > M5_1_closePrev:
                print("short out by candle")
                self.order.oderCloseAllShort()

            # short　closeのタイミング。過去10分間と現状が下がり続けていたら閉じる
            elif M5_1_close < M5_1_closeNow < M5_1_closePrev:
                print("long out by candle")
                self.order.oderCloseAllLong()

            else:
                print('様子見中')

            # 最後にオーダー数を更新する。
            oderSTObj = orderStatus.objects.first()
            oderSTObj.short_order = orderShortNum
            oderSTObj.long_order = orderLongNum
            oderSTObj.save()

            # print(type(condition))

            # 傾きが広がっている＝前の傾きを更新している
            # * 第1ステージ-安定上昇期-すべて傾きが正かつ前よりも傾きの幅が広がっている→買いの仕掛け
            # - 短期>中期>長期
            # * 第2ステージ-下降変化期１上昇相場の終了--**買い清算ポイント**-
            # - 中期>短期>長期
            # * 第3ステージ-下降変化期２下降相場の入り口-売りのはや仕掛け
            # - 中期>長期>短期
            # * 第4ステージ-安定下降期-すべての傾きが負かつ、傾きの幅が広がっている→売りの仕掛け
            # - 長期>中期>短期
            # * 第5ステージ-上昇相場終焉-→売りの手じまい→中長期で幅が広く、すべての傾きがマイナス→戻す可能性あり。
            # - 長期>短期>中期
            # * 第6ステージ-上昇相場の入り口-**買いポイント**-→すべての傾きが正→買いのはや仕掛け
            # - 短期>長期>中期

        else:
            print('お休み中')

        print('----------------------------------------------------------------------------------------------------')
