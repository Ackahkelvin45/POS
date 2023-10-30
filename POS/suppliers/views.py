from django.shortcuts import render, redirect
from .forms import SupplierForm
from django.contrib import messages
from .models import Supplier

# Create your views here.


def showAddSuppliers(request):
    context = {"supplierform": SupplierForm}

    return render(request, "suppliers/addsuppliers.html", context=context)


def addSuppliersProcess(request):
    if request.method == "POST":
        supplierform = SupplierForm(request.POST)
        if supplierform.is_valid():
            supplier = supplierform.save()
            messages.success(request, "Supplier added successfully.")
            return redirect("suppliers:add_supplier")
        else:
            messages.error(request, str(supplierform.errors))

    # If the request method is not POST or the form is not valid, render the same page
    return render(
        request, "suppliers/addsuppliers.html", {"supplierform": supplierform}
    )


def supplierslist(request):
    context = {"suppliers": Supplier.objects.all().order_by("-id")}
    print(context)

    return render(request, "suppliers/supplierslist.html", context=context)
