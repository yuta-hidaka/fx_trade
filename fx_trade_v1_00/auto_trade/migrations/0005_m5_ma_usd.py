# Generated by Django 2.1 on 2019-09-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0004_auto_20190909_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='M5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m5', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('record_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'M5',
            },
        ),
        migrations.CreateModel(
            name='MA_USD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m5_ma5', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma10', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma15', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma20', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma30', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma40', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma50', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma70', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma75', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma140', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('m5_ma150', models.DecimalField(decimal_places=4, default=0.0, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'MA_USD',
            },
        ),
    ]
