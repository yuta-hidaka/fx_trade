# Generated by Django 2.1 on 2019-10-21 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0056_conditionofslope_m5_slope_comp24_75_288'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditionofma_m5',
            name='ma_comp24_75_288',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ma_comp24_75_288', to='auto_trade.listConditionOfMA'),
        ),
        migrations.AlterField(
            model_name='conditionofslope_m5',
            name='slope_comp24_75_288',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slope_comp24_75_288', to='auto_trade.listConditionOfMA'),
        ),
    ]
