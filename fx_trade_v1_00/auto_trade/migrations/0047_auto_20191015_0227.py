# Generated by Django 2.1 on 2019-10-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0046_conditionofbb_is_high_sma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchlog',
            name='text',
            field=models.CharField(max_length=3000),
        ),
    ]
