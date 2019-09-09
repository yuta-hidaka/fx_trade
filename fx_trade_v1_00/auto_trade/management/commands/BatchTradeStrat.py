from ...models import batchRecord
import time
from django.core.management.base import BaseCommand


# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'auto trade batch'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        qSet = batchRecord.objects.filter(id=1).first()
        qSet.text = '最終実行は '+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
        qSet.save()
