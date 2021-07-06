from django.db import models
from django.db.models.fields import CharField
import datetime
import os


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join("uploads/", filename)


class UserAddModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=32)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
