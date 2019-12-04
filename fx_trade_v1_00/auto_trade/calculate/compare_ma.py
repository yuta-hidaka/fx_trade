from ..models import MA_USD_JPY
import numpy as np

# MAを比較する
# 5分足 5本、20本、75本で比較する。

'''受け取った短期、中期、長期のMAを比較してどの状態にいるのかを判断します・'''


class compaireMA():

    def comp3MacdSlope(self, m1, m2, m3):
        '''
        1すべてプラス
        2すべてマイナス
        3すべて０
        4それ以外
        '''
        # 桁数補正
        m1 = m1 * 1000
        m2 = m2 * 1000
        m3 = m3 * 1000

        if m1 >= 0 and m2 >= 0 and m3 >= 0:
            return 1
        elif m1 <= 0 and m2 >= 0 and m3 >= 0:
            return 2
        elif m1 <= 0 and m2 <= 0 and m3 >= 0:
            return 3
        elif m1 <= 0 and m2 <= 0 and m3 <= 0:
            return 4
        elif m1 >= 0 and m2 <= 0 and m3 <= 0:
            return 5
        elif m1 >= 0 and m2 >= 0 and m3 <= 0:
            return 6

        return 0

    def comp3MASlope(self, s, m, l):
        '''
        1すべてプラス
        2すべてマイナス
        3すべて０
        4それ以外
        '''
        slopeList = [s, m, l]
        sumSlope = 0

        if len(set(slopeList)) == len(slopeList):
            return 4

        if slopeList in 0:
            return 4

        for n in slopeList:
            sumSlope += np.sign(n)

        if sumSlope == 3:
            return 1
        elif sumSlope == -3:
            return 2
        elif sumSlope == 0:
            return 3
        else:
            return 4

    def comp3MA(self, s, m, l):
        if s >= m >= l:
            # - 短期>中期>長期
            # print('stage1')
            return 1

        elif m >= s >= l:
            # - 中期>短期>長期
            # print('stage2')
            return 2

        elif m >= l >= s:
            # - 中期>長期>短期
            # print('stage3')
            return 3

        elif l >= m >= s:
            # - 長期>中期>短期
            # print('stage1')
            return 4

        elif l >= s >= m:
            # - 長期>短期>中期
            # print('stage1')
            return 5

        elif s >= l >= m:
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
