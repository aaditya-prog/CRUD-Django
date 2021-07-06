from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .forms import CategoryForm
from .models import CategoryModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(redirect_field_name="")
def categoryAdd(request):
    if request.method == "POST":
        fm = CategoryForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data["category_name"]
            vn = fm.cleaned_data["vendor"]
            data = CategoryModel(category_name=nm, vendor=vn)
            data.save()
            messages.success(request, "New Category Added Successfully.")
            fm = CategoryForm()
        else:
            messages.error(
                request, "Category not added, fill in the details correctly."
            )

    else:
        fm = CategoryForm()

    return render(request, "category/categoryadd.html", {"form": fm})


@login_required(redirect_field_name="")
def categoryRead(request):
    data = CategoryModel.objects.all()
    return render(request, "category/categoryread.html", {"catdata": data})


@login_required(redirect_field_name="")
def delete_category(request, id):
    if request.method == "POST":
        data = CategoryModel.objects.get(pk=id)
        data.delete()
        messages.success(request, "One category deleted successfully")
    return HttpResponseRedirect("/category/categoryread")


@login_required(redirect_field_name="")
def update_category(request, id):
    if request.method == "POST":
        data = CategoryModel.objects.get(pk=id)
        fm = CategoryForm(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Category details updated successfully.")
        else:
            messages.error(request, "Update Failed, try again.")
    else:
        data = CategoryModel.objects.get(pk=id)
        fm = CategoryForm(instance=data)
    return render(request, "category/categoryupdate.html", {"form": fm})
