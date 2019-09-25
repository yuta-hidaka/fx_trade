from ..models import MA_USD_JPY


# MAを比較する
# 5分足 5本、20本、75本で比較する。

'''受け取った短期、中期、長期のMAを比較してどの状態にいるのかを判断します・'''


class compaireMA():
    def comp3MASlope(self, short, middle, long):
        '''
        1すべてプラス
        2すべてマイナス
        3すべて０
        4それ以外
        '''
        slopeList = [short, middle, long]
        sumSlope = 0
        for n in slopeList:
            if n > 0:
                sumSlope += 1
            elif n == 0:
                sumSlope += 0
            else:
                sumSlope += -1

        if sumSlope == 3:
            return 1
        elif sumSlope == -3:
            return 2
        elif sumSlope == 0:
            return 3
        else:
            return 4

    def comp3MA(self, short, middle, long):
        if short > middle > long:
            # - 短期>中期>長期
            # print('stage1')
            return 1

        elif middle > short > long:
            # - 中期>短期>長期
            # print('stage2')
            return 2

        elif middle > long > short:
            # - 中期>長期>短期
            # print('stage3')
            return 3

        elif long > middle > short:
            # - 長期>中期>短期
            # print('stage1')
            return 4

        elif long > short > middle:
            # - 長期>短期>中期
            # print('stage1')
            return 5

        elif short > long > middle:
            # - 短期>長期>中期
            # print('stage6')
            return 6

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
