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
from stock.forms import RecievestockForm
from product.models import Product_Item
from django.urls import reverse

# Create your views here.


def showOrderPage(request):
    
    purchase_order = request.session.get('active_purchase_order')
    
    
   
    
    if   purchase_order:
        purchase_order_item = PurchaseOrder.objects.get(pk=purchase_order)
        context = {
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(instance=purchase_order_item),
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order),
        'purchase_order': purchase_order_item,
       
        
    }
    else:
   
        context = {
            'products': Product_Item.objects.all(),
            'purchaseorderform': PurchaseOrderForm(),
            "suppliers":Supplier.objects.all()
            
        }
    return render(request,'purchases/addpurchaseorder.html',context=context)


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
            if purchase_order.orderedproduct_set.filter(product_id=product_id).exists():
                messages.error(request, 'This product is already in the Purchase Order.You can edit it ')
                return redirect('purchases:order')
        if form.is_valid():
            ordered_product = form.save(commit=False)
            ordered_product.product = product

           
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


def edit_item_process(request,pk):
    if request.method == 'POST':
        product_id = request.POST['product']
        product=Product_Item.objects.get(pk=product_id)
        orderedproduct = OrderedProduct.objects.get(pk=pk)
        
        
        form = OrderedProductForm(request.POST,instance=orderedproduct)
    
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
            

            

def preview_as_pdf(request):
    purchaseorder = PurchaseOrder.objects.get(id=request.session.get('active_purchase_order'))
    tenant=get_tenant(request)
    context = {
         'ordered_products': OrderedProduct.objects.filter(purchase_order=purchaseorder.id),
         "purchaseorder": purchaseorder,
         "pharmacy":tenant
        

    }

    # Render the HTML template
    template = get_template('purchases/purchaseorderpdf.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="product_list.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')

    return response
   


def delete_purchaseorder(request):
    purchaseorder = PurchaseOrder.objects.get(pk=request.session.get('active_purchase_order'))
    del request.session['active_purchase_order']
    purchaseorder.orderedproduct_set.all().delete()
    purchaseorder.delete()
    messages.success(request,'purchase order deleted successfully')
    return redirect('purchases:order')

    

def view_purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()
    context = {
        "purchaseorders":purchase_orders
    }
    return render(request, "purchases/purchaseorderlist.html", context=context)
    
def edit_purchase_order(request, pk):
        purchase_order_item = PurchaseOrder.objects.get(pk=pk)
        context = {
        'products': Product_Item.objects.all(),
        'purchaseorderform': PurchaseOrderForm(instance=purchase_order_item),
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order_item.id),
        'purchase_order': purchase_order_item,
        "suppliers": Supplier.objects.all(),
        "edit":True
        
        
    }
        return render(request, 'purchases/addpurchaseorder.html', context=context)
        



def delete_purchaseorder2(request,pk):
    purchaseorder = PurchaseOrder.objects.get(pk=pk)
    del request.session['active_purchase_order']
    purchaseorder.orderedproduct_set.all().delete()
    purchaseorder.delete()
    messages.success(request,'purchase order deleted successfully')
    return redirect('purchases:purchaseorderlist')



def recieve_order(request, pk):
    purchase_order_item = PurchaseOrder.objects.get(pk=pk)
    context = {
        'ordered_products': OrderedProduct.objects.filter(purchase_order=purchase_order_item.id),
        'purchase_order': purchase_order_item,
        "recievestockform":RecievestockForm(),
       
        
    }
    return render(request, 'purchases/recieve_order.html',context=context)
    




def preview_as_pdf2(request,pk):
    purchaseorder = PurchaseOrder.objects.get(id=pk)
    tenant=get_tenant(request)
    context = {
         'ordered_products': OrderedProduct.objects.filter(purchase_order=purchaseorder.id),
         "purchaseorder": purchaseorder,
         "pharmacy":tenant
        

    }

    # Render the HTML template
    template = get_template('purchases/purchaseorderpdf.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="product_list.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')

    return response
   

def receive_stock_process(request, pk):
    purchase_order = get_object_or_404(PurchaseOrder, id=pk)
    if request.method == 'POST':
        stockform = RecievestockForm(request.POST)
        product = request.POST['product']
        product=get_object_or_404(Product_Item, id=product)

        if stockform.is_valid():
            received_quantity = stockform.cleaned_data['received_quantity']

            if received_quantity < 0:
                messages.error(request, 'Received quantity must be a positive integer.')
                return redirect(reverse("purchases:recieve_order" ,args=[purchase_order.id]))
            elif received_quantity > product.available_quantity:
                messages.error(request, 'Received quantity exceeds available quantity.')
                return redirect(reverse("purchases:recieve_order" ,args=[purchase_order.id]))
            else:
                # Create a ReceivedStock instance
                received_stock = ReceivedStock(
                    purchase_order=purchase_order,
                    product=product,
                    received_quantity=received_quantity
                )
                received_stock.save()

                messages.success(request, f'Stock for {product.name} received successfully.')

                return redirect(reverse("purchases:recieve_order" ,args=[purchase_order.id])) # Redirect to the purchase order list page

        else:
            messages.error(request,str(stockform.errors))
            return redirect(reverse("purchases:recieve_order" ,args=[purchase_order.id]))
      
