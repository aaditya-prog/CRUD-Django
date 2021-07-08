from django.contrib import admin
from django.urls import path, reverse

from . import views

app_name = "user"
urlpatterns = [
    path("", views.UserAdd, name="useradd"),
    path("userread", views.UserRead, name="userread"),
    path("userdelete/<int:id>/", views.deleteUser, name="userdelete"),
    path("<int:id>/", views.update_user, name="userupdate"),
]
