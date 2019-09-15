from ..models import MA_USD_JPY


# MAを比較する
# 5分足 5本、20本、75本で比較する。

'''受け取った短期、中期、長期のMAを比較してどの状態にいるのかを判断します・'''


class compaireMA(self):
    def comp3MA(self, short, middle, long):
        if short > middle > long:
            print('stage1')
            return 1

        elif middle > short > long:
            print('stage2')
            return 2

        elif short > long > middle:
            print('stage3')
            return 3

        elif long > middle > short:
            print('stage1')
            return 4

        elif long > short > middle:
            print('stage1')
            return 5

        elif short > long > middle:
            print('stage6')
            return 6

            # * 第1ステージ-安定上昇期-
            # - 短期>中期>長期
            # * 第2ステージ-下降変化期１上昇相場の終了--**買い清算ポイント**-
            # - 中期>短期>長期
            # * 第3ステージ-下降変化期２下降相場の入り口-
            # - 中期>長期>短期
            # * 第4ステージ-安定下降期-
            # - 長期>中期>短期
            # * 第5ステージ-上昇相場終焉-
            # - 長期>短期>中期
            # * 第6ステージ-上昇相場の入り口-**買いポイント**-
            # - 短期>長期>中期
