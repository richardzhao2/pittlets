# Generated by Django 2.1.3 on 2018-12-06 10:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='', verbose_name='Image')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2018, 12, 6, 5, 14, 5, 303264))),
                ('description', models.TextField(default='', max_length=5000)),
                ('size', models.IntegerField(default=1)),
                ('address', models.CharField(default='', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('location', models.CharField(default='lat: long:', max_length=30)),
                ('amenities', models.CharField(default='ac', max_length=50)),
                ('prorated', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app.Listing'),
        ),
    ]
