# Generated by Django 2.1 on 2019-09-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0015_sellbuyalert'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellbuyalert',
            name='updated_att',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
