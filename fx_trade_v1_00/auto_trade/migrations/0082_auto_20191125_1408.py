# Generated by Django 2.1 on 2019-11-25 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0081_ma_specific_slopema_specific'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ma_specific',
            old_name='m_long',
            new_name='ma_long',
        ),
        migrations.RenameField(
            model_name='ma_specific',
            old_name='m_middle',
            new_name='ma_middle',
        ),
        migrations.RenameField(
            model_name='ma_specific',
            old_name='m_short',
            new_name='ma_short',
        ),
        migrations.AddField(
            model_name='ma_specific',
            name='ms_long',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=8),
        ),
    ]
