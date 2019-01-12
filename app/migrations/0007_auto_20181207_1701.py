# Generated by Django 2.1.3 on 2018-12-07 22:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20181207_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='address',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='listing',
            name='amenities',
            field=models.CharField(default='ac', max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='listing',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 7, 17, 1, 24, 384170)),
        ),
    ]
