# Generated by Django 2.1 on 2019-11-25 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0084_auto_20191125_1421'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='specifcCandle',
            new_name='specificCandle',
        ),
        migrations.AlterModelTable(
            name='specificcandle',
            table='specific_candle',
        ),
    ]
