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

        # トレンド発生中はMAを指標に売買を行うが、もみ合い相場中はボリンジャーバンドを指標に売買を行う。

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

        # 購入するユニット数
        units = 7500
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

        M5_1 = getNowRate.get_5M_now()
        # M5_1 = getNowRate.get_5M_1()

        # 現在の為替情報をその5分10分前の為替の終値を取得する。
        M5_1_close = Decimal(M5_1['candles'][0]['mid']['c'])
        M5_1_closeNow = model_to_dict(condNow.ma.m5)['close']
        M5_1_closePrev = model_to_dict(condiPrev.ma.m5)['close']

        # 市場が閉じていたら計算等は行わない
        if not len(M5_1['candles']) == 0:
            # self.order.orderCreate()
            print('----------------------------------------------------購買条件中------------------------------------------------')
            # 取引条件作成-------------------------------------
            long_in = (
                M5_1_close + M5_1_close*Decimal(0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            long_limit = (
                # M5_1_close + M5_1_close*Decimal(-0.0002)
                M5_1_close + M5_1_close*Decimal(-0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            short_in = (
                M5_1_close + M5_1_close*Decimal(-0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            short_limit = (
                # M5_1_close + M5_1_close*Decimal(0.0002)
                M5_1_close + M5_1_close*Decimal(0.0001)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            self.order.priceLong = str(long_in)
            self.order.stopLossLong = str(long_limit)
            self.order.unitsLong = str(units)

            self.order.priceShort = str(short_in)
            self.order.stopLossShort = str(short_limit)
            self.order.unitsShort = str(units*-1)

            # 購買判断材料-持ち合い形成時--------------------------------------

            # BBから計算したトレンド持ち合い相場だったら下のshortINを使用する。そうでなければMAを使用する。
            trend_id = model_to_dict(condNow.condition_of_bb.bb_trande)['id']
            # もし持ち合い相場だったらこれを使って売買判断None何もしないTrue　shortで入る　False　Longで入る。
            is_shortInBB = model_to_dict(condNow.condition_of_bb)['is_shortIn']

            # 購買判断材料-トレンド形成時--------------------------------------
            maPrev = model_to_dict(
                condiPrev.condition_of_ma_M5
            )['ma_comp5_20_40']

            maNow = model_to_dict(
                condNow.condition_of_ma_M5
            )['ma_comp5_20_40']

            slopePrev = model_to_dict(
                condiPrev.condition_of_slope_M5
            )['slope_comp5_20_40']

            slopeNow = model_to_dict(
                condNow.condition_of_slope_M5
            )['slope_comp5_20_40']

            # 決済タイミングーートレンド形成時-------------------------------------------------------------------------------
            print('maNow')
            print(maNow)
            print('orderLongNum')
            print(orderLongNum)
            print('M5_1_close')
            print(M5_1_close)
            print('M5_1_closeNow')
            print(M5_1_closeNow)

            if maNow == 2 and orderLongNum != 0:
                print("long out by ma")
                self.order.oderCloseAllLong()

                # short　closeのタイミング if MA is 5 it have to close
            elif maNow == 5 and orderShortNum != 0:
                print("short out by ma")
                self.order.oderCloseAllShort()

                # short　closeのタイミング。過去10分間と現状が上がり続けていたら閉じる
            elif M5_1_close > M5_1_closeNow and orderShortNum != 0:
                print("short out by candle")
                self.order.oderCloseAllShort()

                # long　closeのタイミング。過去10分間と現状が下がり続けていたら閉じる
            elif M5_1_close < M5_1_closeNow and orderLongNum != 0:
                print("long out by candle")
                self.order.oderCloseAllLong()

            else:
                print('決済----様子見中')

            # 上昇or下降トレンド相場だったら
            if trend_id == 1:
                print('BB---上昇相場')
            elif trend_id == 2:
                print('BB---下降相場')

            if trend_id == 1 or trend_id == 2:
                # 購買タイミング----------------------------------------------------------------------------------
                # longのタイミング all slope is positive and before MA is 6or1 and now 1
                if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
                    if not orderLongNum > 1:
                        print("long in 以下short order数")
                        orderLongNum += 1

                        self.order.LongOrderCreate()
                    else:
                        print("long in　but position is too many")
                        # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
                elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                    if not orderShortNum > 1:
                        print("short in")
                        orderShortNum += 1
                        self.order.ShortOrderCreate()
                    else:
                        print("short in　but position is too many")

                        # long closeのタイミング if MA is 2 it have to close
                else:
                    print('購買----様子見中')

                    # --------------------------------------------------------------------------------------------------------------------

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
                # 購買タイミング
                # longのタイミング all slope is positive and before MA is 6or1 and now 1
                if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
                    if not orderLongNum > 1:
                        print("long in 以下__1624")
                        orderLongNum += 1
                        self.order.LongOrderCreate()

                    else:
                        print("long in　but position is too many__1624")

                        # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
                elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                    if not orderShortNum > 1:
                        print("short in　以下__1624")
                        orderShortNum += 1
                        self.order.ShortOrderCreate()
                    else:
                        print("short in　but position is too many__1624")

                        # long closeのタイミング if MA is 2 it have to close
                else:
                    print('購買----様子見中__1624')

            # 持ち合い相場だったら
            elif trend_id == 3:
                print('持ち合い相場')
                if is_shortInBB == True:
                    print('持ち合い相場の逆張りshort_inーー同時にlong決済も行う')
                    if orderLongNum != 0:
                        print('long決済')
                        self.order.oderCloseAllLong()
                    if not orderShortNum > 1:
                        self.order.ShortOrderCreate()
                    else:
                        print('注文リミット')

                elif is_shortInBB == False:
                    print('持ち合い相場の逆張りlong_in--同時にshort決済も行う。')
                    if orderShortNum != 0:
                        print('short決済')
                        self.order.oderCloseAllShort()
                    if not orderLongNum > 1:
                        self.order.LongOrderCreate()
                    else:
                        print('注文リミット')
                else:
                    print('BB持ち合い時の購買サイン出ていない')

                    # それ以外
            else:
                print('trend_idがないから何もしない')

    # --------------------------------------------------------------------------------------------------------------------

            # 最後にオーダー数を更新する。
            oderSTObj = orderStatus.objects.first()
            oderSTObj.short_order = orderShortNum
            oderSTObj.long_order = orderLongNum
            oderSTObj.save()

        else:
            print('お休み中')

        print('-----------------------------------------------購買条件中-終了----------------------------------------------------')
