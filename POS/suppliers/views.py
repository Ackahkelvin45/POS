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
        'suppliers':Supplier.objects.all ().order_by('-id')
    }

    return render(request,'suppliers/supplierslist.html',context=context)



def delete_supplier(request, pk):
    if Supplier.objects.filter(id=pk).exists():
        supplier =Supplier.objects.get(id=pk)
        supplier.delete()
        messages.success(request, 'Supplier Deleted Successfully')
        return redirect("suppliers:supplierlist")
    messages.error(request, 'Error Try Agian')
    return redirect("suppliers:supplierlist")




def edit_supplier(request, pk):
    if Supplier.objects.filter(id=pk).exists():
        supplier = Supplier.objects.get(id=pk)
        context = {
              "supplier": Supplier.objects.all().order_by('-id'),
                'supplierform': SupplierForm(instance=supplier),
                "edit": True,
                'supplier_item':supplier
        }
        return render(request, 'suppliers/addsuppliers.html', context=context)
        

def edit_supplier_process(request, pk):
    if request.method == "POST":
        if Supplier.objects.filter(id=pk).exists():
            supplier= Supplier.objects.get(id=pk)
            supplierform = SupplierForm(request.POST,instance=supplier)
            if supplierform.is_valid():
                supplier = supplierform.save()
                messages.success(request, 'Supplier Edited Successfully')
                return redirect("suppliers:supplierlist")
            messages.error(request, str(supplierform.errors))
            return redirect("suppliers:supplierlist")
