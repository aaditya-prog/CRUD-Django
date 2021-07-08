from django.db import models


# Create your models here.
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=50)
    vendor = models.CharField(max_length=50)
