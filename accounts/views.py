from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import (
    DjangoUnicodeDecodeError,
    force_bytes,
    force_str,
    force_text,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import AddImageForm, RegisterForm
from .models import CustomUser, Profile
from .utlis import generate_token
from django.contrib.auth.decorators import login_required


def login_excluded(redirect_to):
    """This decorator kicks authenticated users out of a view"""

    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper


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


@login_excluded("user:userread")
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


@login_excluded("user:userread")
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


def accounts(request):
    userdata = CustomUser.objects.all()
    return render(
        request, "accounts/manage/accounts.html", {"userdata": userdata}
    )


def delete_account(request, id):
    if request.method == "POST":
        data = CustomUser.objects.get(pk=id)
        data.delete()
        return HttpResponseRedirect("/accounts/")


def update_account(request, id):
    if request.method == "POST":
        data = CustomUser.objects.get(pk=id)
        fm = RegisterForm(request.POST, instance=data)
        if fm.is_valid():
            fm.set_password(Password)
            fm.save()
            messages.success(request, "User details updated successfully.")
        else:
            messages.error(request, "Update Failed, try again.")
    else:
        data = CustomUser.objects.get(pk=id)
        fm = RegisterForm(instance=data)
    return render(request, "accounts/manage/update.html", {"form": fm})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")


@login_required(redirect_field_name="")
def user_change_pass(request):
    if request.method == "POST":
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password changed successfully.")
            update_session_auth_hash(request, fm.user)
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, "accounts/password/changepass.html", {"form": fm})


@login_required(redirect_field_name="")
def profile(request):
    if request.method == "POST":
        fm = AddImageForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if fm.is_valid():
            fm.save()
            messages.success(request, "Profile Picture Updated")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Could not upload image, try again.")
    else:
        fm = AddImageForm()
    return render(request, "accounts/profile.html", {"form": fm})


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified, login to continue.")
        return redirect(reverse("accounts:login"))
    else:
        return render(request, "accounts/activate-failed.html", {"user": user})
