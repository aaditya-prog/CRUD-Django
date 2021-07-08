from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UserAddForm
from .models import UserAddModel


# Add User
@login_required(redirect_field_name="")
def UserAdd(request):
    if request.method == "POST":
        fm = UserAddForm(request.POST)

        if fm.is_valid():
            nm = fm.cleaned_data["name"]
            ad = fm.cleaned_data["address"]
            em = fm.cleaned_data["email"]
            pw = fm.cleaned_data["password"]
            img = fm.cleaned_data["image"]
            usradd = UserAddModel(
                name=nm, email=em, address=ad, password=pw, image=img
            )
            usradd.save()
            fm = UserAddForm()
            messages.success(request, "User added successfully.")

        else:
            messages.error(
                request,
                "Could not register user, the details are not filled"
                " properly.",
            )
    else:
        fm = UserAddForm()
    return render(request, "user/useradd.html", {"form": fm})


# Retrive user data from database
@login_required(redirect_field_name="")
def UserRead(request):
    userdata = UserAddModel.objects.all()
    return render(request, "user/userread.html", {"userdata": userdata})


# delete user data
@login_required(redirect_field_name="")
def deleteUser(request, id):
    if request.method == "POST":
        data = UserAddModel.objects.get(pk=id)
        data.delete()
        messages.success(request, "User deleted successfully.")
    return HttpResponseRedirect("/user/userread")


# update
@login_required(redirect_field_name="")
def update_user(request, id):
    if request.method == "POST":
        data = UserAddModel.objects.get(pk=id)
        fm = UserAddForm(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
            messages.success(request, "User details updated successfully.")
        else:
            messages.error(request, "Update Failed, try again.")
    else:
        data = UserAddModel.objects.get(pk=id)
        fm = UserAddForm(instance=data)
    return render(request, "user/userupdate.html", {"form": fm})
