# Generated by Django 2.1 on 2019-09-10 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0005_m5_ma_usd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='m5',
            old_name='m5',
            new_name='close',
        ),
        migrations.AddField(
            model_name='m5',
            name='high',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='m5',
            name='low',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8),
        ),
        migrations.AddField(
            model_name='m5',
            name='open',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8),
        ),
    ]
