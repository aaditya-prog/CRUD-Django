from django.contrib import admin
from .models import CustomUser, BaseUserManager

admin.site.register(CustomUser)
