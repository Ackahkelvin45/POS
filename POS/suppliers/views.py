from django.shortcuts import render, redirect
from .forms import SupplierForm
from django.contrib import messages
from .models import Supplier
import pandas as pd
from io import BytesIO
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django_tenants.utils import get_tenant
import pdfkit
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='tenant:login')
def showAddSuppliers(request):
    context = {"supplierform": SupplierForm}

    return render(request, "suppliers/addsuppliers.html", context=context)

@login_required(login_url='tenant:login')
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

@login_required(login_url='tenant:login')
def supplierslist(request):
    context = {"suppliers": Supplier.objects.all().order_by("-id")}
    return render(request, "suppliers/supplierslist.html", context=context)



@login_required(login_url='tenant:login')
def export_suppliers_as_pdf(request):
    template = get_template('suppliers/suppliers_pdf.html')  
    html_content = template.render({
        'suppliers': Supplier.objects.all().order_by("-id"),
        "pharmacy":get_tenant(request)
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="supliers.pdf"'
    return response




@login_required(login_url='tenant:login')
def delete_supplier(request, pk):
    if Supplier.objects.filter(id=pk).exists():
        supplier =Supplier.objects.get(id=pk)
        supplier.delete()
        messages.success(request, 'Supplier Deleted Successfully')
        return redirect("suppliers:supplierlist")
    messages.error(request, 'Error Try Agian')
    return redirect("suppliers:supplierlist")



@login_required(login_url='tenant:login')
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
        
@login_required(login_url='tenant:login')
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



 