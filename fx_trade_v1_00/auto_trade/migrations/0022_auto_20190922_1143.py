# Generated by Django 2.1 on 2019-09-22 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0021_auto_20190921_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conditionofma_m5',
            name='ma_comp5_20_75',
        ),
        migrations.AddField(
            model_name='condition',
            name='conditiond',
            field=models.CharField(default='', max_length=256),
        ),
    ]
