from django import forms
from django.contrib.messages.api import error
from django.forms import widgets

from .models import UserAddModel


class UserAddForm(forms.ModelForm):
    class Meta:
        model = UserAddModel
        fields = ["name", "address", "email", "password", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter name",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter address",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter email",
                }
            ),
            "password": forms.PasswordInput(
                render_value=True,
                attrs={
                    "class": "form-group form-control w-25 p-3",
                    "Placeholder": "Enter password",
                },
            ),
            "image": forms.FileInput(
                attrs={
                    "help_text": "Add image",
                    "class": "form-group form-control-file",
                    "Placeholder": "Upload Image",
                }
            ),
        }

        error_messages = {
            "name": {"required": "You must provide your name"},
            "address": {"required": "You must enter your address"},
            "email": {
                "required": "You must enter your email for contact purposes"
            },
            "password": {
                "required": "You must provide an appropriate password"
            },
            "image": {"required": "Error: user image required"},
        }
