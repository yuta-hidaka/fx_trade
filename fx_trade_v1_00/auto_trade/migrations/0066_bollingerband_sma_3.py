# Generated by Django 2.1 on 2019-10-22 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0065_auto_20191022_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='bollingerband',
            name='sma_3',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8, null=True),
        ),
    ]
