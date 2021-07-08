from django.contrib import admin

from .models import UserAddModel


# Register your models here.
@admin.register(UserAddModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "email", "password", "image")
