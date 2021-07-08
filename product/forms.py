from django import forms

from .models import productModel


class ProductForm(forms.ModelForm):
    class Meta:
        model = productModel
        fields = ["name", "quantity", "stock", "price", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter product name",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter quantity",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter stock",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter price",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-group form-control-file",
                    "Placeholder": "Upload Image",
                }
            ),
        }

        error_messages = {
            "name": {"required": "You must provide the product's name"},
            "quantity": {"required": "You must enter the quantity"},
            "stock": {"required": "You didn't specify the stock"},
            "price": {"required": "Price must be mentioned"},
            "image": {"required": "Error: user image required"},
        }
