# Generated by Django 2.1 on 2019-12-10 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0098_auto_20191210_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='condition_of_slope_M5ssss',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conditionOfSlope_M5ssss', to='auto_trade.conditionOfSlope_M5'),
        ),
    ]
