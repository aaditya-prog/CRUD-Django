from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.utils.encoding import (
    force_bytes,
    force_str,
    force_text,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utlis import generate_token
from django.template.loader import render_to_string


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Complete your registration"
    email_body = render_to_string(
        "accounts/activate.html",
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": generate_token.make_token(user),
        },
    )

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        to=[
            user.email,
        ],
    )

    email.send()


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
            user = CustomUser(
                email=Email,
                full_name=Name,
                address=Address,
                password=Password,
            )
            user.is_active = False
            user.set_password(Password)
            user.save()
            send_activation_email(user, request)
            messages.success(
                request,
                "User registration successful, an email has been sent to you,"
                " Verify to login.",
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
            if not user.is_active:
                messages.error(
                    request,
                    "Your email has not been verified yet, verify your email"
                    " first.",
                )
                return render(request, "accounts/login.html", {"form": fm})
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


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified")
        return redirect(reverse("accounts:login"))
    else:
        return render(request, "accounts/activate-failed.html", {"user": user})
