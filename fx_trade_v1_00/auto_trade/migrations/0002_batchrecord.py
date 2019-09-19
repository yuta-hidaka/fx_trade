# Generated by Django 2.1 on 2019-09-09 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='batchRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'batch_record',
            },
        ),
    ]
