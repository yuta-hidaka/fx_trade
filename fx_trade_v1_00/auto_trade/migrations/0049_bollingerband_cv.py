# Generated by Django 2.1 on 2019-10-18 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0048_conditionofbb_is_peak'),
    ]

    operations = [
        migrations.AddField(
            model_name='bollingerband',
            name='cv',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8, null=True),
        ),
    ]
