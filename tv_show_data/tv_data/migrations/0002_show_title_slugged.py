# Generated by Django 2.1.7 on 2019-05-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='title_slugged',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
