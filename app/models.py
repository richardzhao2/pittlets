from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Listing(models.Model):
    title = models.CharField(max_length = 200, default = '')
    pub_date = models.DateTimeField(default=datetime.now())
    description = models.TextField(max_length = 5000, default = '')
    size = models.IntegerField(default = 1)
    address = models.CharField(max_length = 80, default = '')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.CharField(max_length=100, default='ac')
    prorated = models.BooleanField(default = False)
    type = models.CharField(max_length = 30, default = 'n/a')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Image(models.Model):
    post = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images', default = None)
    photo = models.ImageField(verbose_name = 'Image')
