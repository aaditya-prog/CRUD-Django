from django.contrib import admin
from django.urls import path

from . import views

app_name = "product"
urlpatterns = [
    path("", views.productAdd, name="productadd"),
    path("productread", views.ProductView, name="productread"),
    path("deleteproduct/<int:id>", views.delete_product, name="deleteproduct"),
    path("<int:id>", views.update_product, name="updateproduct"),
]
