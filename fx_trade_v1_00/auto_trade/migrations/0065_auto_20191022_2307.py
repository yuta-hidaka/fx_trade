# Generated by Django 2.1 on 2019-10-22 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0064_remove_bollingerband_sma'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bollingerband',
            old_name='sma_M50',
            new_name='sma',
        ),
    ]
