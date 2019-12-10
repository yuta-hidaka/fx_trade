# Generated by Django 2.1 on 2019-12-10 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0091_tradesettings_use_trailing_stop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condition',
            name='condition_of_bb',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='condition_of_ma_M5',
        ),
        migrations.RemoveField(
            model_name='condition',
            name='condition_of_slope_M5',
        ),
        migrations.AlterField(
            model_name='condition',
            name='ma',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='condition_ma', to='auto_trade.MA_Specific'),
        ),
    ]
