from django.contrib import admin
from .models import CategoryModel


@admin.register(CategoryModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ["category_name", "vendor"]
