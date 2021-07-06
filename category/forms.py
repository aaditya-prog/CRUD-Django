from django import forms
from django.forms import widgets
from .models import CategoryModel


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ["category_name", "vendor"]
        widgets = {
            "category_name": forms.TextInput(
                attrs={
                    "class": "form-group form-control w-25",
                    "Placeholder": "Enter category name",
                }
            ),
            "vendor": forms.TextInput(
                attrs={
                    "class": " form-group form-control w-25",
                    "Placeholder": "Enter vendor name",
                }
            ),
        }
        error_messages = {
            "category_name": {"required": "You must enter the category's name"},
            "vendor": {"required": "Error: vendor required"},
        }
