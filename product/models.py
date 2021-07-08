import datetime
import os

from django.db import models
from django.db.models.fields import CharField


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join("uploads/", filename)


class productModel(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    stock = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
