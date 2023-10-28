from django.shortcuts import render,redirect
from .forms import SupplierForm
from django.contrib import messages
from .models import Supplier
# Create your views here.

def showAddSuppliers(request):
    context = {
        'supplierform':SupplierForm
    }

    return render(request, 'suppliers/addsuppliers.html', context=context)
    

def addSuppliersProcess(request):
    if request.method == 'POST':
        supplierform = SupplierForm(request.POST)
        if supplierform.is_valid():
            supplier = supplierform.save()
            messages.success(request, 'Supplier added Successfully')
            return redirect("suppliers:add_supplier")
        messages.success(request, str(supplierform.errors))
        return redirect("suppliers:add_supplier")
            

def supplierslist(request):
    context = {
        'suppliers':Supplier.objects.al().order_by('-id')
    }

    return render(request,'suppliers/supplierslist.html',context=context)