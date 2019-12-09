from ..models import MA_USD_JPY, orderStatus, batchLog, tradeSettings, conditionOfSlope_M5, MA_Specific, conditionOfMA_M5
from django.forms.models import model_to_dict
from ..service.get_MA_USD_JPY import getMA_USD_JPY
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
from fx_trade_v1_00.lib.access_token import FxInfo
from fx_trade_v1_00.lib.order import orderFx
import json
from decimal import *
import numpy as np

from django.utils import timezone
import datetime

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

    def BuySellCheck(self, condNow, condiPrev, spec):
        # トレンド発生中はMAを指標に売買を行うが、もみ合い相場中はボリンジャーバンドを指標に売買を行う。

        settings = self.settings
        self.order.useTrailing = settings.use_trailing_stop
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
        sig2_2 = bb['abs_sigma_2_2']
        sig1_2 = bb['abs_sigma_1_2']
        sma_2 = bb['sma_2']

        nowCndl = getNowRate.get_now()
        # nowCndl = getNowRate.get_5M_1()

        # 現在の為替情報とその5分10分前の為替の終値を取得する。
        nowCndl_close = Decimal(nowCndl['candles'][0]['mid']['c'])
        self.order.priceNow = nowCndl_close
        # self.order.LongOrderCreate()
        # print(nowCndl_close)
        M5_1_closeNow = model_to_dict(condNow.ma.m5)['close']
        M5_1_closePrev = model_to_dict(condiPrev.ma.m5)['close']

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

        # ----------------------------------------------------------------
        macd1 = spec.macd1
        macd2 = spec.macd2
        macd3 = spec.macd3

        specMa = spec.compMa
        specEma = spec.compEma
        specMacd = spec.compMacd

        specMaSlope = spec.compMaSlope
        specEmaSlope = spec.compEmaSlope
        specMacdSlope = spec.compMacdSlope
        # ----------------------------------------------------------------

        try:
            useCnt = settings.use_cnt
            pass
        except:
            self.text += 'eraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa<br>'
            useCnt = False
            pass

        if settings.use_specific_limit:
            limit = settings.limit
            c = nowCndl_close
            long_limit = (c - (c*limit)).quantize(Decimal('0.001'),
                                                  rounding=ROUND_HALF_UP)
            short_limit = (
                c + (c*limit)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        else:
            limit = sig1_2
            long_limit = (sma_2 - limit).quantize(Decimal('0.001'),
                                                  rounding=ROUND_HALF_UP)
            short_limit = (
                sma_2 + limit).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

        long_in_by_ma = False
        short_in_by_ma = False

        # 購入するユニット数
        # units = 7500
        try:
            units = settings.units
            # units = 1
            pass
        except:
            self.text += '予期しないロット数が入っています'
            units = 1
            pass

        # 市場が閉じていたら計算等は行わない,変化率が乏しい時もトレードしない
        if not len(nowCndl['candles']) == 0:
            # self.order.orderCreate()
            # print('----------------------------------------------------購買条件中------------------------------------------------')
            # 取引条件作成-------------------------------------
            long_in = (
                nowCndl_close + nowCndl_close*Decimal(0.00025)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # long_limit = (bb['sma'] - bb['abs_sigma_3']
            #               ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            short_in = (
                nowCndl_close - nowCndl_close*Decimal(0.00025)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            # BBから計算したトレンド持ち合い相場だったら下のshortINを使用する。そうでなければMAを使用する。
            trend_id = model_to_dict(
                condNow.condition_of_bb.bb_trande
            )['id']

            preTrend_id = model_to_dict(
                condiPrev.condition_of_bb.bb_trande
            )['id']

            self.order.trend_id = trend_id

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

            self.order.priceLong = str(long_in)
            self.order.stopLossLong = str(long_limit)
            self.order.unitsLong = str(units)

            self.order.priceShort = str(short_in)
            self.order.stopLossShort = str(short_limit)
            self.order.unitsShort = str(units*-1)
            # 前回までトレンドで今が持ち合い相場であればいったん決済する。

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
                # print('何かエラー起きてます。')
                trend_id = 1
                pass

                # --------------------------------------------------------------------------------------------------------------------
            self.text += 'トレンドID　' + str(trend_id) + '<br>'

            now = timezone.now()
            adjTime = datetime.timedelta(minutes=15)
            sTime = now - adjTime

            # ----------------------------------------------------------------------------------------------------------

            # emaCheckLong = [6]
            # emaCheckShort = [3]
            # macdCheckLong = [6]
            # macdCheckShort = [3]

            emaCheckLong = [6, 1]
            emaCheckShort = [3, 4]

            macdCheckLong = [1, 6]
            macdCheckShort = [3, 4]
            # self.order.isInByMa = True
            # self.order.trend_id = 1
            # self.order.LongOrderCreate()
            if specEma in emaCheckLong:
                # self.text += 'long in--emaCheck<br>'
                if specEmaSlope == 1 and specMacdSlope == 1:
                    self.text += 'long in by macd<br>'
                    rs = MA_Specific.objects.filter(compEma=4).filter(
                        created_at__range=(sTime, now)).order_by('-id').count()
                    self.text += str(rs) + \
                        '--この4がありました--<br>'
                    if not useCnt:
                        rs = 0
                    if rs == 0:
                        self.order.isInByMa = True
                        self.order.trend_id = 1
                        self.order.LongOrderCreate()

            elif specEma in emaCheckShort:
                if specEmaSlope == 2 and specMacdSlope == 2:
                    self.text += 'short in by macd<br>'

                    if not useCnt:
                        rs = 0
                    if rs == 0:
                        self.order.isInByMa = True
                        self.order.trend_id = 2
                        self.order.ShortOrderCreate()

            if specEma == 5 or specEma == 6:
                self.text = 'specMaが'+str(specEma)+'なのでshortを閉じます<br>'
                self.order.oderCloseAllShort()
            elif specEma == 3 or specEma == 4:
                self.text = 'specMaが'+str(specEma)+'なのでLongを閉じます<br>'
                self.order.oderCloseAllLong()

            self.text += 'specMa ' + str(specMa)+'<br>'
            self.text += 'specEma ' + str(specEma)+'<br>'
            self.text += 'specMacdSlope ' + str(specMacdSlope)+'<br>'
            self.text += 'specSlope ' + str(specMaSlope)+'<br>'
            self.text += 'macd1 ' + str(macd1)+'<br>'
            self.text += 'macd2 ' + str(macd2)+'<br>'
            self.text += 'macd3 ' + str(macd3)+'<br>'
            self.text += 'specEma ' + str(specEma)+'<br>'
            self.text += 'specMacd ' + str(specMacd)+'<br>'
            self.text += 'is_expansion ' + str(is_expansion)+'<br>'

            ls = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ls = [1, 2, 3, 4, 5, 6]

            for l in ls:
                rs = MA_Specific.objects.filter(compEma=l).filter(
                    created_at__range=(sTime, now)).order_by('-id').count()
                self.text += '※※※※※※※※※※※※※※※※'+str(rs) + \
                    'この' + str(l)+'がありました※※※※※※※※※※※※※※※※<br>'

            # if specMacd == 1 and specEmaSlope != 4:
            #     self.text = 'specMaが6なのでshortを閉じます<br>'
            #     self.order.oderCloseAllShort()
            # elif specMacd == 4 and specEmaSlope != 4:
            #     self.text = 'specMaが3なのでLongを閉じます<br>'
            #     self.order.oderCloseAllLong()

            # m3 = (macd3).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            # if m3 == 0:
            #     self.text = 'macd3が0なのですべて閉じます。<br>'
            #     self.order.allOrderClose()

            # -------------------------------------------------------------------------------------------------------

            # if maPrev == 6 or maPrev == 1 and maNow == 1 and slopeNow == 1:
            #     rs = conditionOfMA_M5.objects.filter(
            #         ma_comp6_24_72=4).filter(
            #         created_at__range=(sTime, now)).order_by('-id').count()
            #     self.text += 'long in by ma休止中<br>'
            #     self.text += str(rs)+'この4がありました※※※※※※※※※※※※※※※※<br>'
            #     self.text += str(rs)+str(trend_id)+'sinma<br>'

            #     # 過去15分の間に4が3以上存在したら購買しない
            #     if rs == 0:
            #         if not settings.use_specific_limit:
            #             limit = sig3_2

            #         if trend_id != 4:
            #             self.order.isInByMa = True
            #             long_limit = (
            #                 sma_2 - limit).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #             self.order.stopLossLong = str(long_limit)
            #             self.order.trend_id = 1
            #             # self.order.LongOrderCreate()
            #         else:
            #             # print('long in　but position is too many')
            #             self.text += 'long in by ma trend idが4なので様子見です<br>'
            #             # shorのタイミング all slope is negative and befor MA is 3or4 and now 4
            #     else:
            #         self.text += '<p style="color=red;">最近4が1つ以上ありました or trendじゃない</p>'

            # elif maPrev == 3 or maPrev == 4 and maNow == 4 and slopeNow == 2:
            #     rs = conditionOfMA_M5.objects.filter(
            #         ma_comp6_24_72=1).filter(
            #         created_at__range=(sTime, now)).order_by('-id').count()
            #     self.text += 'short in by ma休止中<br>'
            #     self.text += str(rs)+'この1がありました※※※※※※※※※※※※※※※※<br>'
            #     self.text += str(rs)+str(trend_id)+'sinma<br>'

            #     if not settings.use_specific_limit:
            #         limit = sig3_2

            #     # 過去15分の間に1が3以上存在したら購買しない
            #     if rs == 0:
            #         if trend_id != 4:
            #             self.order.isInByMa = True
            #             short_limit = (
            #                 sma_2 + limit).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
            #             self.order.stopLossShort = str(short_limit)
            #             self.order.trend_id = 2
            #             # self.order.ShortOrderCreate()
            #         else:
            #             # print('short in　but position is too many')
            #             self.text += 'short in by ma trend idが4なので様子見です<br>'
            #             # long closeのタイミング if MA is 2 it have to close
            #     else:
            #         self.text += '<p style="color=red;">最近1が1つ以上ありましたor trendじゃない</p>'
            # else:
            #     self.text += '購買----様子見中 MAでの購買判定<br>'

            # # if self.order.lossCutReverse():
            # #     self.text += 'lossCutReverseで購入<br>'

    # --------------------------------------------------------------------------
            trend_id = 0
            if trend_id == 1 or trend_id == 2 or trend_id == 4 and not is_peak:
                self.text += 'トレンド相場------------------------------------------------<br>'

                # 決済タイミングーートレンド形成時-------------------------------------------------------------------------------
                if maNow == 2 and trend_id != 1:
                    self.text += 'long out by ma休止中<br>'
                    # if not :
                    #     self.order.oderCloseAllLong()

                    # short　closeのタイミング if MA is 5 it have to close
                elif maNow == 5 and trend_id != 2:
                    self.text += 'short out by ma休止中<br>'
                    # if not :
                    #     self.order.oderCloseAllShort()

            # 持ち合い相場でエクスパンションしてなかったら

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

            if trend_id == 3 and cv <= 75:
                self.text += '持ち合い相場<br>'
                try:
                    tlogCondiId = self.order.tlog.condition_id
                    pass
                except:
                    tlogCondiId = 0
                    pass

                self.text += 'self.order.tlog.condition_id ' + \
                    str(tlogCondiId)+'<br>'
                if not is_expansion:
                    # if is_shortClose:
                    #     if tlogCondiId == 3:
                    #         self.text += 'sigma1 によるshortClose<br>'
                    #         self.order.oderCloseAllShort()

                    # elif is_longClose:
                    #     if tlogCondiId == 3:
                    #         self.text += 'sigma1 によるlongClose<br>'
                    #         self.order.oderCloseAllLong()

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
            #     self.text += '持ち合い lossCutReverseの処理を試行<br>'
            #     if self.order.lossCutReverse():
            #         self.text += 'lossCutReverseで購入<br>'
            # else:
            #     self.text += 'トレンドなのでlossCutReverseでの購入を行わない<br>'
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
