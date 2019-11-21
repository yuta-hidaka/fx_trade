from ..models import MA_USD_JPY, orderStatus, batchLog, tradeSettings
from django.forms.models import model_to_dict
from ..service.get_MA_USD_JPY import getMA_USD_JPY
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
from fx_trade_v1_00.lib.access_token import FxInfo
from fx_trade_v1_00.lib.order import orderFx
import json
from decimal import *
import numpy as np

# MAを比較する
# 5分足 5本、20本、75本で比較する。

'''受け取った短期、中期、長期のMAを比較してどの状態にいるのかを判断します・'''


class BuySellCal():
    def __init__(self):
        self.fx = FxInfo()
        self.order = orderFx()
        self.settings = tradeSettings.objects.filter(id=1).first()
        self.order.waitTime = self.settings.wait_time
        self.text = ''

    def BuySellCheck(self, condNow, condiPrev):

        # トレンド発生中はMAを指標に売買を行うが、もみ合い相場中はボリンジャーバンドを指標に売買を行う。

        # # print(json.dumps(pos),  indent=2)
        settings = self.settings
        getNowRate = getMA_USD_JPY()

        cbb = model_to_dict(condNow.condition_of_bb)
        cbbPrev = model_to_dict(condiPrev.condition_of_bb)

        bb = model_to_dict(condNow.condition_of_bb.bb)
        bbPrev = model_to_dict(condiPrev.condition_of_bb.bb)
        # もし持ち合い相場だったらこれを使って売買判断None何もしないTrue　shortで入る　False　Longで入る。
        is_shortInBB = cbb['is_shortIn']
        is_longInBB = cbb['is_longIn']
        is_expansion = cbb['is_expansion']
        is_topTouch = cbb['is_topTouch']
        is_bottomTouch = cbb['is_bottomTouch']
        cv = bb['cv'] * Decimal(1000000)
        # 上位足のσ2をma購買リミットにする
        sig3_2 = bb['abs_sigma_3_2']

        # 持ち合い時には下位足の標準偏差のσ2を使用する
        sig2 = bb['abs_sigma_2']


        self.text += 'cv  ' + str(cv) + '<br>'
        is_peak = cbb['is_peak']
        is_shortClose = cbb['is_shortClose']
        is_longClose = cbb['is_longClose']

        is_expansionByStd = cbb['is_expansionByStd']
        is_expansionByNum = cbb['is_expansionByNum']

        is_expansionPrev = cbbPrev['is_expansion']
        is_expansionByStdPrev = cbbPrev['is_expansionByStd']
        is_expansionByNumPrev = cbbPrev['is_expansionByNum']
        is_topTouchPrev = cbbPrev['is_topTouch']
        is_bottomTouchPrev = cbbPrev['is_bottomTouch']


        if settings.use_specific_limit:
            limit = settings.limit
        else:
            limit = sig2

        long_in_by_ma = False
        short_in_by_ma = False

        # 購入するユニット数
        # units = 7500
        try:
            units = settings.units
            pass
        except:
            self.text += '予期しないロット数が入っています'
            units = 1
            pass

        nowCndl = getNowRate.get_now()
        # nowCndl = getNowRate.get_5M_1()

        # 現在の為替情報とその5分10分前の為替の終値を取得する。
        nowCndl_close = Decimal(nowCndl['candles'][0]['mid']['c'])
        M5_1_closeNow = model_to_dict(condNow.ma.m5)['close']
        M5_1_closePrev = model_to_dict(condiPrev.ma.m5)['close']

        # 市場が閉じていたら計算等は行わない,変化率が乏しい時もトレードしない
        if not len(nowCndl['candles']) == 0:
            # self.order.orderCreate()
            # print('----------------------------------------------------購買条件中------------------------------------------------')
            # 取引条件作成-------------------------------------
            long_in = (
                nowCndl_close + nowCndl_close*Decimal(0.00015)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # long_limit = (bb['sma'] - bb['abs_sigma_3']
            #               ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            short_in = (
                nowCndl_close - nowCndl_close*Decimal(0.00015)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # short_limit = (bb['sma'] + bb['abs_sigma_3']
            #                ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            long_limit = (nowCndl_close - (nowCndl_close * limit)
                          ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            short_limit = (nowCndl_close + (nowCndl_close * limit)
                           ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # lDeff = np.abs(long_in - long_limit)
            # if lDeff < 0.1:
            #     long_limit = (nowCndl_close - Decimal(0.115)
            #                   ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #     self.text += 'longのlimitが小さいので修正<br>'
            # elif lDeff > 0.115:
            #     long_limit = (nowCndl_close - Decimal(0.115)
            #                   ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #     self.text += 'longのlimitが大きいので修正<br>'

            # sDeff = np.abs(short_in - short_limit)
            # if sDeff < 0.1:
            #     short_limit = (nowCndl_close + Decimal(0.115)
            #                    ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #     self.text += 'shortのlimitが小さいので修正<br>'
            # elif sDeff > 0.115:
            #     short_limit = (nowCndl_close + Decimal(0.115)
            #                    ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #     self.text += 'shortのlimitが大きいので修正<br>'

            # 購買タイミング----------------------------------------------------------------------------------
            # longのタイミング all slope is positive and before MA is 6or1 and now 1

            # BBから計算したトレンド持ち合い相場だったら下のshortINを使用する。そうでなければMAを使用する。
            trend_id = model_to_dict(
                condNow.condition_of_bb.bb_trande
            )['id']

            preTrend_id = model_to_dict(
                condiPrev.condition_of_bb.bb_trande
            )['id']

            self.order.trend_id = trend_id

            # if not is_expansionPrev and is_expansion and is_expansionByStd or is_expansionByNum:
            #     self.text += '確度が小さいのでlimit小さく<br>'
            #     # 確度が小さいのでlimit小さく
            #     long_limit = (nowCndl_close - ((nowCndl_close * limit/2))
            #                   ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #     short_limit = (nowCndl_close + ((nowCndl_close * limit/2))
            #                    ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # self.text += 'longの入り値　' + str(long_in) + '<br>'
            # self.text += 'longの損切　' + str(long_limit) + '<br>'
            # self.text += 'longの差　' + str(long_in - long_limit) + '<br>'
            # self.text += 'shortの入り値　' + str(short_in) + '<br>'
            # self.text += 'shortの損切　' + str(short_limit) + '<br>'
            # self.text += 'shortの差　' + str(short_in - short_limit) + '<br>'

            # if self.order.lossCutCheck(False, False):
            #      = True
            #      = True
            # (
            #     # M5_1_close + M5_1_close*Decimal(0.0002)
            #     M5_1_close + M5_1_close*Decimal(0.003)
            # ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # 購買判断材料-持ち合い形成時--------------------------------------

            # 購買判断材料-トレンド形成時--------------------------------------

            # 上昇or下降トレンド相場だったら
            if trend_id == 1:
                # print('BB---上昇相場')
                self.text += 'BB---上昇相場<br>'
            elif trend_id == 2:
                # print('BB---下降相場')
                self.text += 'BB---下降相場<br>'
            elif trend_id == 3:
                # print('BB---持ち合い相場')
                self.text += 'BB---持ち合い相場<br>'
            elif trend_id == 4:
                # print('BB---持ち合い相場')
                self.text += 'BB---トレンドだけど傾きが逆<br>'

                # self.text += 'is_bottomTouch<br>'
                # self.text += str(is_bottomTouch) + '<br>'
                # self.text += 'is_topTouch<br>'
                # self.text += str(is_topTouch) + '<br>'
                # self.text += 'not is_expansion<br> '
                # self.text += str(not is_expansion) + '<br>'
                # self.text += 'is_expansion<br> '
                # self.text += str(is_expansion) + '<br>'
                # self.text += 'is_expansionByStd<br> '
                # self.text += str(is_expansionByStd) + '<br>'
                # self.text += 'is_expansionByNum<br> '
                # self.text += str(is_expansionByNum) + '<br>'

            self.order.priceLong = str(long_in)
            self.order.stopLossLong = str(long_limit)
            self.order.unitsLong = str(units)

            self.order.priceShort = str(short_in)
            self.order.stopLossShort = str(short_limit)
            self.order.unitsShort = str(units*-1)
            # 前回までトレンドで今が持ち合い相場であればいったん決済する。


                # エクスパンションしているか
                # if is_expansion:
            if self.order.lossCutReverse():
                self.text += "lossCutReverseで購入<br>"

            try:
                # print(condNow.condition_of_bb.bb_trande)

                maPrev = model_to_dict(
                    condiPrev.condition_of_ma_M5
                )['ma_comp6_24_72']

                maNow = model_to_dict(
                    condNow.condition_of_ma_M5
                )['ma_comp6_24_72']

                slopePrev = model_to_dict(
                    condiPrev.condition_of_slope_M5
                )['slope_comp6_24_72']

                slopeNow = model_to_dict(
                    condNow.condition_of_slope_M5
                )['slope_comp6_24_72']

                pass
            except Exception as e:
                self.text += str(e)+' error　error<br>'
                maPrev = 1
                maNow = 1
                slopePrev = 1
                slopeNow = 1
                # print("何かエラー起きてます。")
                trend_id = 1
                pass

                # --------------------------------------------------------------------------------------------------------------------
            self.text += 'トレンドID　' + str(trend_id) + '<br>'
            # if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
            #     if trend_id != 4:
            #         # print("long in by ma")
            #         self.text += "long in by ma<br>"
                    # self.isInByMa = True

            #         self.order.LongOrderCreate()
            #         self.order.trend_id = 1
            #     else:
            #         # print("long in　but position is too many")
            #         self.text += "long in by ma trend idが4なので様子見です<br>"
            #         # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
                    
            # elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
            #     if trend_id != 4:
            #         # self.order.oderCloseAllLong()
            #         # print("short in by ma")
            #         self.text += "short in by ma<br>"
                    # self.isInByMa = True
            #         self.order.ShortOrderCreate()
            #         self.order.trend_id = 2
            #     else:
            #         # print("short in　but position is too many")
            #         self.text += "short in by ma trend idが4なので様子見です<br>"
            #         # long closeのタイミング if MA is 2 it have to close
            # else:
            #     # print('購買----様子見中')
            #     self.text += '購買----様子見中 MAでの購買判定<br>'

            if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
                if not settings.use_specific_limit:
                    limit = sig3_2
                
                if trend_id != 4:
                    long_limit = (nowCndl_close - (nowCndl_close * (limit))).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
                    self.order.stopLossLong = str(long_limit)
                    self.text += "long in by ma<br>"
                    self.isInByMa = True
                    self.order.LongOrderCreate()
                else:
                    # print("long in　but position is too many")
                    self.text += "long in by ma trend idが4なので様子見です<br>"
                    # shorのタイミング all slope is negative and befor MA is 3or4 and now 4

            elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                if not settings.use_specific_limit:
                    limit = sig3_2

                if trend_id != 4:
                    short_limit = (nowCndl_close + (nowCndl_close * (limit))).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
                    self.order.stopLossShort = str(short_limit)
                    self.text += "short in by ma<br>"
                    self.isInByMa = True
                    self.order.ShortOrderCreate()
                else:
                    # print("short in　but position is too many")
                    self.text += "short in by ma trend idが4なので様子見です<br>"
                    # long closeのタイミング if MA is 2 it have to close
            else:
                # print('購買----様子見中')
                self.text += '購買----様子見中 MAでの購買判定<br>'

    # --------------------------------------------------------------------------
            if trend_id == 1 or trend_id == 2 or trend_id == 4 and not is_peak:
                self.text += "トレンド相場------------------------------------------------<br>"

                # if is_longInBB:

                # elif is_shortInBB:

                # if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1 and not  and not :
                #     if not  and not trend_id == 4:
                #         # print("long in by ma")
                #         text += "long in by ma<br>"
                #          = self.order.LongOrderCreate()
                #     else:
                #         # print("long in　but position is too many")
                #         text += "long in　but position is too many<br>"
                #         # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
                # elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                #     if not  and not trend_id == 4:
                #         # self.order.oderCloseAllLong()
                #         # print("short in by ma")
                #         text += "short in by ma<br>"
                #          = self.order.ShortOrderCreate()
                #     else:
                #         # print("short in　but position is too many")
                #         text += "short in　but position is too many<br>"
                #         # long closeのタイミング if MA is 2 it have to close
                # else:
                #     # print('購買----様子見中')
                #     text += '購買----様子見中 MAでの購買判定<br>'

                # 決済タイミングーートレンド形成時-------------------------------------------------------------------------------
                if maNow == 2 and trend_id != 1:
                    # print("long out by ma")
                    self.text += "long out by ma休止中<br>"
                    # if not :
                    #     self.order.oderCloseAllLong()

                    # short　closeのタイミング if MA is 5 it have to close
                elif maNow == 5 and trend_id != 2:
                    # print("short out by ma")
                    self.text += "short out by ma休止中<br>"
                    # if not :
                    #     self.order.oderCloseAllShort()

                #     # long　closeのタイミング。過去10分間と現状が下がり続けていたら閉じる
                # elif M5_1_closePrev > nowCndl_close > M5_1_closeNow and trend_id != 1 :
                #     # print("long out by candle")
                #     self.text += "long out by candle<br>"
                #     if not :
                #         self.order.oderCloseAllLong()

                #     # short　closeのタイミング。過去10分間と現状が上がり続けていたら閉じる
                # elif M5_1_closePrev < nowCndl_close < M5_1_closeNow and trend_id != 2 :
                #     # print("short out by candle")
                #     self.text += "short out by candle<br>"
                #     if not :
                #         self.order.oderCloseAllShort()
                # else:
                #     # print('決済----様子見中')
                #     self.text += '上下降トレンドの決済様子見中<br>'

                # 購買タイミング
                # longのタイミング all slope is positive and before MA is 6or1 and now 1
                # if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
                #     if  == 0:
                #         print("long in 以下__1624")
                #          += 1
                #         self.order.LongOrderCreate()
                #          = True

                #     else:
                #         print("long in　but position is too many__1624")

                #         # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
                # elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
                #     if  == 0:
                #         print("short in　以下__1624")
                #          += 1
                #         self.order.ShortOrderCreate()
                #          = True

                #     else:
                #         print("short in　but position is too many__1624")

                #         # long closeのタイミング if MA is 2 it have to close
                # else:
                #     print('購買----様子見中__1624')

                # if trend_id == 1:
                #     # long_limit = (nowCndl_close - (nowCndl_close * Decimal(0.002))
                #     #               ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
                #     # self.order.stopLossLong = str(long_limit)
                #     if not :
                #         # print("long in by ma")
                #         self.text += "BB算出の上昇トレンド、long,弱気<br>"
                #         self.order.LongOrderCreate()
                #          = True
                #     else:
                #         # print("long in　but position is too many")
                #         self.text += "long in　but position is too many<br>"
                #         # shorのタイミング all slope is negative and befor MA is 3or4 and now 4

                # elif trend_id == 2:
                #     # short_limit = (nowCndl_close + (nowCndl_close * Decimal(0.002))
                #     #                ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
                #     # self.order.stopLossShort = str(short_limit)
                #     if  not :
                #             # self.order.oderCloseAllLong()
                #             # print("short in by ma")
                #             self.text += "BB算出の下降トレンド、short,弱気<br>"
                #             self.order.ShortOrderCreate()
                #              = True
                #     else:
                #             # print("short in　but position is too many")
                #             self.text += "short in　but position is too many<br>"

            # 持ち合い相場でエクスパンションしてなかったら

            if is_peak:
                self.text += 'sigma3 エクスパンションの底値。ポジションを入れ替える 休止中<br>'
                if is_bottomTouch:
                    self.text += 'sigma3 エクスパンション終了で下タッチなのでlongIn　休止中<br>'
                    # self.order.LongOrderCreate()

                elif is_topTouch:
                    self.text += 'sigma3 エクスパンション終了で上タッチなのでshortIn　休止中<br>'
                    # self.order.ShortOrderCreate()

            if trend_id == 3 and not is_peak:
                # if preTrend_id == 1 or preTrend_id == 2 or preTrend_id == 4:
                #         self.text += '前回までトレンドで今が持ち合い相場でいったん決済。<br>'
                #         self.order.allOrderClose()
                # 偏差と数値によるエクスパンションで確度が高めのポジションを持つ
                if not is_expansionPrev and is_expansion and is_expansionByStd and is_expansionByNum:
                    self.text += 'エクスパンション確度が高め　休止中<br>'
                    if is_topTouch:
                        # print('エクスパンションで上タッチなので買い')
                        self.text += 'エクスパンションで上タッチなのでLong by Std<br>'
                        # self.order.LongOrderCreate()
                    elif is_bottomTouch:
                        # print('エクスパンションで下タッチなので売り')
                        self.text += 'エクスパンションで下タッチなのでShort by Std<br>'
                        # self.order.ShortOrderCreate()
                    else:
                        self.text += 'エクスパンションbyStd_購買条件未該当<br>'

                # 前回エクスパンションしていなかったら初めてのエクスパンションとする,
                # 偏差によるエクスパンションでなければlong、short両方のポジションを持つ
                elif not is_expansionPrev and is_expansion and is_expansionByStd or is_expansionByNum:
                    self.text += 'エクスパンションbyNum or Std<br>'
                    if is_topTouch:
                        self.text += 'エクスパンションorだましで上タッチのLongIn　休止中<br>'
                        # self.order.LongOrderCreate()

                    elif is_bottomTouch:
                        self.text += 'エクスパンションorだましで上タッチなのでshortIn　休止中<br>'
                        # self.order.ShortOrderCreate()
                        self.text += 'ShortIn<br>'

                    else:
                        self.text += 'エクスパンションorだまし_購買条件未該当<br>'

                    # 前回エクスパンションしていて、いまエクスパンションが収まったら、底の認識でそれぞれ売り払って逆方向にinする
                # elif is_expansionPrev and not is_expansion and is_expansionByStdPrev:
                #     self.text += 'エクスパンションの底値。ポジションを入れ替える <br>'
                #     if is_bottomTouch or is_bottomTouchPrev:
                #         self.text += 'エクスパンション終了で下タッチなのでlongIn<br>'
                #         self.order.LongOrderCreate()
                #          = True

                #     elif is_topTouch or is_topTouchPrev:
                #         self.text += 'エクスパンション終了で上タッチなのでshortIn<br>'
                #         self.order.ShortOrderCreate()
                #          = True

            if trend_id == 3:
                if not is_expansion:
                    if is_shortClose:
                        self.text += 'sigma1 によるshortClose<br>'
                        self.order.oderCloseAllShort()

                    elif is_longClose:
                        self.text += 'sigma1 によるlongClose<br>'
                        self.order.oderCloseAllLong()
                    self.text += '持ち合い相場<br>'

                    if is_topTouch:
                        self.text += '持ち合い相場の逆張りshort_inーー同時にlong決済も行う<br>'
                        self.order.ShortOrderCreate()
                        # print('注文リミット')
                    elif is_bottomTouch:
                        # print('持ち合い相場の逆張りlong_in--同時にshort決済も行う。')
                        self.text += '持ち合い相場の逆張りlong_in--同時にshort決済も行う。<br>'
                        self.order.LongOrderCreate()

                    else:
                        # print('BB持ち合い時の購買サイン出ていない')
                        self.text += 'BB持ち合い時の購買サイン出ていない<br>'

                        # それ以外
                elif trend_id == 4:
                    # print('サイン出てない')
                    self.text += 'サイン出てない 傾きが0なので様子見中<br>'

                else:
                    self.text += 'エクスパンション中<br>'
            else:
                 self.text += 'サイン出てない<br>'
                # --------------------------------------------------------------------------
            # # self.order.ShortOrderCreate()
            # checkRange = [3, 5]
            # if trend_id in checkRange:
            #     self.text += "持ち合い lossCutReverseの処理を試行<br>"
            #     if self.order.lossCutReverse():
            #         self.text += "lossCutReverseで購入<br>"
            # else:
            #     self.text += "トレンドなのでlossCutReverseでの購入を行わない<br>"
            self.text += '<br>-------------------------------ここからorderの内容----------------------------------<br>' + self.order.text
    # --------------------------------------------------------------------------------------------------------------------

            # # 最後にオーダー数を更新する。
            # oderSTObj = orderStatus.objects.first()
            # oderSTObj.short_order =
            # oderSTObj.long_order =
            # oderSTObj.save()

            # batchLog.objects.create(text=text)

        else:
            print('お休み中')

            # print('-----------------------------------------------購買条件中-終了----------------------------------------------------')

        # # print(model_to_dict(condition))
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

        # # print(type(condition))

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
