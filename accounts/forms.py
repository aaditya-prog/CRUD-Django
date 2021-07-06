from django import forms
from .models import CustomUser
from django.contrib.auth import password_validation


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser

        fields = ["full_name", "address", "email", "password"]

        labels = {
            "full_name": "Full Name",
            "email": "Email",
            "password": "Password",
            "address": "Address",
        }

        help_text = {
            "password": "Include numbers for better security",
        }

        error_messages = {
            "full_name": {"required": "you must enter your name"},
            "address": {"required": "You must provide a valid address"},
            "password": {"required": "You must enter your password"},
            "email": {"required": "Email required for verification"},
        }

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "John Doe",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "user@example.com",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Kathmandu, Nepal",
                }
            ),
            "password": forms.PasswordInput(
                attrs={"placeholder": "Include numbers for better security"}
            ),
        }

