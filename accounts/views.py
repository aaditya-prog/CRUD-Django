from django.shortcuts import render, HttpResponseRedirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.views.generic import View
from django.utils.encoding import (
    force_bytes,
    force_text,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utlis import token_generator


def register(request):
    if request.method == "POST":
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            Name = fm.cleaned_data["full_name"]
            Address = fm.cleaned_data["address"]
            Email = fm.cleaned_data["email"]
            Password = fm.cleaned_data["password"]
            if len(Name) < 4:
                raise ValidationError(
                    "Invalid Name, enter a valid name and try again."
                )
            if len(Address) < 4:
                raise ValidationError(
                    "Invalid Address, enter a valid address and try again."
                )
            if len(Email) < 10:
                raise ValidationError(
                    "Invalid Name, enter a valid name and try again."
                )
            account = CustomUser(
                email=Email,
                full_name=Name,
                address=Address,
                password=Password,
            )
            # account.is_active = False
            account.set_password(Password)
            account.save()
            # path_to_view
            # getting domain we are on
            # relative url to verification
            # encode uid
            # token (one tiem use)
            # current_site = get_current_site(request)
            # email_body = {
            #     "domain": current_site.domain,
            #     "uid": urlsafe_base64_encode(force_bytes(CustomUser.pk)),
            #     "token": token_generator.make_token(CustomUser),
            # }
            # link = reverse(
            #     "accounts:activate",
            #     kwargs={
            #         "uidb64": email_body["uid"],
            #         "token": email_body["token"],
            #     },
            # )
            # activate_url = "http://" + current_site.domain + link
            # email_body = (
            #     "Please use this link to verify your account/n" + activate_url
            # )
            # email_subject = "Complete your registration"
            # email = EmailMessage(
            #     email_subject,
            #     email_body,
            #     "noreply@crud.com",
            #     [Email],
            # )
            # email.send(fail_silently=False)
            messages.success(
                request, "User registration successful, login to continue."
            )
        else:
            messages.error(request, "registration failed, try again.")
    else:
        fm = RegisterForm()
    return render(request, "accounts/register.html", {"form": fm})


def user_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            un = fm.cleaned_data["username"]
            pw = fm.cleaned_data["password"]
            user = authenticate(username=un, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/user/")
    else:
        fm = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")


def user_change_pass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password changed successfully.")
            update_session_auth_hash(request, fm.user)
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, "accounts/changepass.html", {"form": fm})


def profile(request):
    return render(request, "accounts/profile.html")


class VerificationView(View):
    def get(self, request, uid, token):
        return HttpResponseRedirect("accounts/login")
