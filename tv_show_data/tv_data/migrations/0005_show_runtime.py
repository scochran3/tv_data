# Generated by Django 2.1.7 on 2019-06-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv_data', '0004_auto_20190527_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='runtime',
            field=models.IntegerField(default=22),
        ),
    ]
