# Generated by Django 2.1.3 on 2018-12-06 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181206_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 6, 5, 30, 38, 946131)),
        ),
    ]