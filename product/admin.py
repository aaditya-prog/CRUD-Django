from django.contrib import admin

from .models import productModel


# Register your models here.
@admin.register(productModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "quantity", "stock", "price", "image")
