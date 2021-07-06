from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ProductForm
from .models import productModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(redirect_field_name="")
def productAdd(request):
    if request.method == "POST":
        frm = ProductForm(request.POST)
        if frm.is_valid():
            nm = frm.cleaned_data["name"]
            qt = frm.cleaned_data["quantity"]
            st = frm.cleaned_data["stock"]
            pr = frm.cleaned_data["price"]
            img = frm.cleaned_data["image"]
            product = productModel(
                name=nm, quantity=qt, stock=st, price=pr, image=img
            )
            product.save()
            frm = ProductForm()
            messages.success(request, "Product added successfully.")

        else:
            messages.error(request, "Fill the form correctly and try again.")
    else:
        frm = ProductForm()
    return render(request, "product/productadd.html", {"form": frm})


@login_required(redirect_field_name="")
def ProductView(request):
    productdata = productModel.objects.all()
    return render(request, "product/productread.html", {"data": productdata})


@login_required(redirect_field_name="")
def delete_product(request, id):
    if request.method == "POST":
        data = productModel.objects.get(pk=id)
        data.delete()
        messages.success(request, "Product successfully deleted.")
    return HttpResponseRedirect("/product/productread")


@login_required(redirect_field_name="")
def update_product(request, id):
    if request.method == "POST":
        data = productModel.objects.get(pk=id)
        fm = ProductForm(request.POST, instance=data)
        if fm.is_valid():
            fm.save()
            messages.success(request, "User details updated successfully.")
        else:
            messages.error(request, "Update Failed, try again.")
    else:
        data = productModel.objects.get(pk=id)
        fm = ProductForm(instance=data)
    return render(request, "product/productupdate.html", {"form": fm})
