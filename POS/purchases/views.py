
from django.shortcuts import render,redirect,get_object_or_404
from product.models import Product_Item, Package
from suppliers.models import Supplier
from .forms import PurchaseOrderForm,OrderedProductForm
from django.http import JsonResponse
from django.core import serializers
import json
from .models import PurchaseOrder,OrderedProduct
from django.contrib import messages
import pandas as pd
from io import BytesIO
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django_tenants.utils import get_tenant
from django.urls import reverse
from stock.models import StockEntry
from  settings.models import EmailBackend, AppSettings
from django.core.mail import EmailMessage
import pdfkit
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='tenant:login')
def showOrderPage(request):
    
    purchase_order = request.session.get('active_purchase_order')
    tenant = get_tenant(request)
    setting = AppSettings.objects.first()
    
    
   
    
    if purchase_order:
        
        purchase_order_item = PurchaseOrder.objects.get(pk=purchase_order)
        context = {
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(instance=purchase_order_item),
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order),
        'purchase_order': purchase_order_item,
        'setting':setting
       
       
        
    }
    else:
   
        context = {
            'products': Product_Item.objects.all(),
            'purchaseorderform': PurchaseOrderForm(),
            "suppliers": Supplier.objects.all(),
            'setting':setting
       
            
        }
    return render(request,'purchases/addpurchaseorder.html',context=context)
@login_required(login_url='tenant:login')
def remove_from_session(request):
    if 'active_purchase_order' in request.session:
        del request.session['active_purchase_order']           
        return redirect('purchases:order')
    return redirect('purchases:order')


@login_required(login_url='tenant:login')
def searchProduct(request):
     if request.method == "POST":
        product_name = request.POST['product_name']
        product_name = product_name.strip()
        product_chosed =products.objects.filter(name=product_name)
        context = {
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(),
        'products_chosed':product_chosed,
            

        }
        return render(request,'purchases/addpurchaseorder.html',context=context)



@login_required(login_url='tenant:login')
def search_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name', '')
        try:
            products = Product_Item.objects.filter(name__icontains=product_name)
            data = serializers.serialize('json', products)
            data_list = json.loads(data)
        
            return JsonResponse(data_list, safe=False)
        except Product_Item.DoesNotExist:
          
            return JsonResponse({'error': 'Product not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='tenant:login')
def order_item(request, pk):
    product = Product_Item.objects.get(pk=pk)
    packages = Package.objects.filter(product_id=product.id)
    product_form = OrderedProductForm(initial={'product': product})
   
    context = {
        "product": product,
        'packages':packages, 
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(),
        'modal': True,
        "productform":product_form
        
    }
    return render(request, 'purchases/addpurchaseorder.html', context=context)
    

@login_required(login_url='tenant:login')
def purchase_item(request):
    

    # Check if there is an active PurchaseOrder for the session
    purchase_order = request.session.get('active_purchase_order')
    purchase_order_item = PurchaseOrder(pk=purchase_order)
    print(purchase_order )
    

    if request.method == 'POST':
        product_id = request.POST['product']
        product=Product_Item.objects.get(pk=product_id)
        
        form = OrderedProductForm(request.POST)
        if purchase_order:
            purchase_order = PurchaseOrder.objects.get(pk=purchase_order)

        if form.is_valid():
            ordered_product = form.save(commit=False)
            ordered_product.product = product
            ordered_product.calculate_total_cost_price()
            ordered_product.calculate_quantity()
            if purchase_order:
                if purchase_order.orderedproduct_set.filter(product_id=ordered_product.product.id ,package_type=ordered_product.package_type ).exists():
                    messages.error(request, 'This product is already in the Purchase Order.You can edit it ')
                    return redirect('purchases:order')

           
            if purchase_order:
                purchase_order=PurchaseOrder.objects.get(pk=purchase_order.id)
                ordered_product.purchase_order = purchase_order
                ordered_product.save()
                purchase_order.save()

            
            if not purchase_order:
                purchase_order = PurchaseOrder(creator=request.user)
                purchase_order.save()
                request.session['active_purchase_order'] = purchase_order.pk
                ordered_product.purchase_order = purchase_order
                ordered_product.save()
                purchase_order.save()
            messages.success(request,'product added successfully')
            return redirect('purchases:order')
        messages.error(request, str(form.errors))
        print(form.errors)
        return redirect('purchases:order')

    context = {
        "product": product,
        'packages': packages,
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(),
        'modal': True,
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order),
        'purchase_order': purchase_order,
    }
    return render(request, 'purchases/addpurchaseorder.html', context=context)

        

@login_required(login_url='tenant:login')
def delete_ordered_product(request, pk):
    product = OrderedProduct.objects.get(pk=pk)
    if product.purchase_order and product.purchase_order.orderedproduct_set.count() <= 1:      
        if 'active_purchase_order' in request.session:
            del request.session['active_purchase_order']
            po=product.purchase_order
            product.delete()
            po.delete()
            messages.success(request,'product removed successfully')
            return redirect('purchases:order')
    else:
        product.delete()
        messages.success(request,'product removed successfully')
        return redirect('purchases:order')

@login_required(login_url='tenant:login') 
def edit_item(request, pk):
    product_item = OrderedProduct.objects.get(pk=pk)
    packages = Package.objects.filter(product_id=product_item.product.id)
    product_form = OrderedProductForm(initial={'product': product_item.product})
   
    context = {
        "product": product_item.product,
        'packages':packages, 
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(),
        'modal': True,
        "productform": product_form,
        "orderedproduct": product_item,
        "edit":True
        
    }
    return render(request, 'purchases/addpurchaseorder.html', context=context)

@login_required(login_url='tenant:login')
def edit_item_process(request,pk):
    if request.method == 'POST':
        product_id = request.POST['product']
        product=Product_Item.objects.get(pk=product_id)
        orderedproduct = OrderedProduct.objects.get(pk=pk)
        
        
        form = OrderedProductForm(request.POST,instance=orderedproduct,)
    
        if form.is_valid():
            ordered_product = form.save(commit=False)
            ordered_product.product = product
            ordered_product.save()
            purchaseorder = ordered_product.purchase_order
            purchaseorder.save()
      

            messages.success(request,'product edited successfully')
            return redirect('purchases:order')
        messages.error(request,str(form.errors))
        return redirect('purchases:order')

@login_required(login_url='tenant:login')
def save_purchase_order(request):
    if request.method == "POST":
        purchase_order = PurchaseOrder.objects.get(id=request.session.get('active_purchase_order'))
        purchaseorderform = PurchaseOrderForm(request.POST, instance=purchase_order)
        if purchaseorderform.is_valid():
            purchaseorder = purchaseorderform.save(commit=True)       
            messages.success(request,'purchase order saved  successfully')
            return redirect('purchases:order')
        messages.error(request,str(purchaseorderform.errors))
        return redirect('purchases:order')
            

            
@login_required(login_url='tenant:login')
def preview_as_pdf(request):
    purchaseorder = PurchaseOrder.objects.get(id=request.session.get('active_purchase_order'))
    tenant=get_tenant(request)
    template = get_template('purchases/purchaseorderpdf.html')  
    html_content = template.render({
       'ordered_products': OrderedProduct.objects.filter(purchase_order=purchaseorder.id),
         "purchaseorder": purchaseorder,
         "pharmacy":tenant
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="products.pdf"'
    return response
   

@login_required(login_url='tenant:login')
def delete_purchaseorder(request):
    purchaseorder = PurchaseOrder.objects.get(pk=request.session.get('active_purchase_order'))
    del request.session['active_purchase_order']
    purchaseorder.orderedproduct_set.all().delete()
    purchaseorder.delete()
    messages.success(request,'purchase order deleted successfully')
    return redirect('purchases:order')

    
@login_required(login_url='tenant:login')
def view_purchase_order_list(request):
    context = {
        "purchaseorders":PurchaseOrder.objects.all().order_by("-id")
    }
    return render(request, "purchases/purchaseorderlist.html", context=context)
@login_required(login_url='tenant:login')   
def edit_purchase_order(request, pk):
        purchase_order_item = PurchaseOrder.objects.get(pk=pk)
        request.session['active_purchase_order'] = purchase_order_item.id
        context = {
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(instance=purchase_order_item),
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order_item.id),
        'purchase_order': purchase_order_item,
        "suppliers": Supplier.objects.all(),
        "edit":True
        
        
    }
        return render(request, 'purchases/addpurchaseorder.html', context=context)
        


@login_required(login_url='tenant:login')
def delete_purchaseorder2(request,pk):
    purchaseorder = PurchaseOrder.objects.get(pk=pk)
    del request.session['active_purchase_order']
    purchaseorder.orderedproduct_set.all().delete()
    purchaseorder.delete()
    messages.success(request,'purchase order deleted successfully')
    return redirect('purchases:purchaseorderlist')


@login_required(login_url='tenant:login')
def recieve_order(request, pk):
    purchase_order_item = PurchaseOrder.objects.get(pk=pk)
    context = {
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order_item.id).order_by('id'),
        'purchase_order': purchase_order_item,

       
        
    }
    return render(request, 'purchases/recieve_order.html',context=context)
    



@login_required(login_url='tenant:login')
def preview_as_pdf2(request,pk):
    purchaseorder = PurchaseOrder.objects.get(id=pk)
    tenant=get_tenant(request)
    template = get_template('purchases/purchaseorderpdf.html')  
    html_content = template.render({
       'ordered_products': OrderedProduct.objects.filter(purchase_order=purchaseorder.id),
         "purchaseorder": purchaseorder,
         "pharmacy":tenant
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="products.pdf"'
    return response
   
   
@login_required(login_url='tenant:login')
def receive_stock_process(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)
    if request.method == 'POST':
        recieved_quantity=request.POST['recieved_quantity']
        orderedproduct = request.POST['orderedproduct']
        date = request.POST['received_date']
        receive_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        orderedproduct = get_object_or_404(OrderedProduct, id=orderedproduct)
        if int(recieved_quantity) > 0:
            if int(recieved_quantity) <= orderedproduct.remaining_quantity:
                orderedproduct.received_quantity = orderedproduct.received_quantity + int(recieved_quantity)
                orderedproduct.add_to_stock(user=request.user,quantity=int(recieved_quantity),date=receive_date)
                purchase_order.update_order_status()
                if orderedproduct.package_type:
                    messages.success(request, f'{str(recieved_quantity)} {orderedproduct.package_type} {str(orderedproduct.product.name)} recieved sucessfully')
                    return redirect(reverse('purchases:recieve_order',args=[pk]))
                messages.success(request, f'{str(recieved_quantity)}  {str(orderedproduct.product.name)} recieved sucessfully')
                return redirect(reverse('purchases:recieve_order',args=[pk]))

            messages.error(request, 'recieved quantity can not be greater to remaining quantity')
            return redirect(reverse('purchases:recieve_order',args=[pk]))

        
        messages.error(request, f'recieved quantity can not be {str(recieved_quantity)}')
        return redirect(reverse('purchases:recieve_order',args=[pk]))



@login_required(login_url='tenant:login')
def recieve_all_stock(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)
    orderedproduct = OrderedProduct.objects.filter(purchase_order=purchase_order.id)
    for product in orderedproduct:
        product.recieved_quantity = product.remaining_quantity
        product.add_to_stock(user=request.user,quantity=int(product.recieved_quantity ))
    purchase_order.update_order_status()
    messages.success(request, 'All items recievd succesfully')
    return redirect(reverse('purchases:recieve_order',args=[pk]))      

@login_required(login_url='tenant:login')
def send_purhase_order_as_email(request, pk):
    purchaseorder = PurchaseOrder.objects.get(id=request.session.get('active_purchase_order'))
    tenant=get_tenant(request)
    template = get_template('purchases/purchaseorderpdf.html')  
    html_content = template.render({
       'ordered_products': OrderedProduct.objects.filter(purchase_order=purchaseorder.id),
         "purchaseorder": purchaseorder,
         "pharmacy":tenant
    
    })  

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-images': False,
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    email_user = EmailBackend.objects.order_by('pk').first()
   
    email = EmailMessage(
                            'Purchase Order',
                            "Purchase Order",
                            email_user.email,
                            [purchaseorder.supplier.email,]

                        )
    email.attach('purchase_order.pdf', pdf_data, 'application/pdf')
    email.fail_silently = False
    email.send()
    messages.success(request, 'Purchase Order sent  succesfully')
    return redirect('purchases:order') 
            
@login_required(login_url='tenant:login')   
def get_costprice_of_package(request):
    package_id = request.GET.get('package_id', None)

    try:
        package =  Package.objects.get(pk=package_id)
        cost_price = package.cost_price
        data = {'result': 'success', 'cost_price': cost_price}
    except :
        data = {'result': 'error', 'message': 'Product not found'}

    return JsonResponse(data)