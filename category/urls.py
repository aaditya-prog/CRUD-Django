from django.contrib import admin
from django.urls import path

from . import views

app_name = "category"
urlpatterns = [
    path("", views.categoryAdd, name="categoryadd"),
    path("categoryread", views.categoryRead, name="categoryread"),
    path("deletecategory/<int:id>", views.delete_category, name="deletecategory"),
    path("<int:id>/", views.update_category, name="categoryupdate"),
]
