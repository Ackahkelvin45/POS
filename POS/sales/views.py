from django.shortcuts import render,redirect
from product.models import Product_Item,Package
from django.http import JsonResponse
from django.core import serializers
import json
from .forms import SaleForm, SaleProductForm,TaxForm,PaymentDetailsForm
from .models import Sale, SaleProduct,Tax,PausedSale
from django.contrib import messages
from decimal import Decimal
from django.template.loader import get_template
from django_tenants.utils import get_tenant
from django.http import HttpResponse
import pdfkit
from datetime import datetime
from django.utils import timezone
from settings.models import AppSettings
from django.views import View
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='tenant:login')
def show_add_sales(request):
    sale = request.session.get('active_sale')
    setting = AppSettings.objects.first()
    if sale:
   
        
        sale_item = Sale.objects.get(pk=sale)
        context = {
        'products': Product_Item.objects.all(),
        'saleform':SaleForm(instance=sale_item,allow_date_change_value=setting.allow_date_change),
        'saleproducts': SaleProduct.objects.filter(sale=sale).order_by("-id"),
        'sale': sale_item,
        'taxform': TaxForm(),
        'taxes': Tax.objects.all(),
        "paymentform": PaymentDetailsForm(initial={"sale": sale_item}),
        'setting':setting
       
        
    }
    else:
   
        context = {
            'products': Product_Item.objects.all(),
            'saleform': SaleForm(allow_date_change_value=setting.allow_date_change),
            'taxform': TaxForm(),
            "taxes": Tax.objects.all(),
            "paymentform": PaymentDetailsForm(),
            'setting':setting
           
            
        }
 
    return render(request, 'sales/addsales.html',context=context)


@login_required(login_url='tenant:login')
def show_sales_history(request):
    context = {
        "sales":Sale.objects.filter(status="completed").order_by('-id')
    }
    return render(request, "sales/saleshistory.html",context=context)
    


class GetPackageCostView(View):
    def get(self, request, *args, **kwargs):
        try:
            package_id = request.GET.get('package_id')
            package = Package.objects.get(pk=package_id)
            cost_price= package.selling_price

            
            return JsonResponse({'selling_price': cost_price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GetProductCostView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_id= request.GET.get('product_id')
            product = Product_Item.objects.get(pk=product_id)
            cost_price= product.selling_price

            
            return JsonResponse({'selling_price': cost_price})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
    saleform = SaleProductForm(initial={'product': product})
   
    context = {
        "product": product,
        'products': Product_Item.objects.all(),
        'modal': True,
        "saleform":saleform
        
    }
    return render(request, 'sales/addsales.html', context=context)

@login_required(login_url='tenant:login')
def sell_item(request):
    
    sale= request.session.get('active_sale')
    sale_item = Sale(pk=sale)
  
    if request.method == 'POST':
        product_id = request.POST['product']
        product=Product_Item.objects.get(pk=product_id)
        
        form = SaleProductForm(request.POST)

            
        if form.is_valid():
            saleproduct = form.save(commit=False)
    
            if sale:
                sale = Sale.objects.get(pk=sale)
                if saleproduct.package_type:

                    if   sale.saleproduct_set.filter(package_type_id=saleproduct.package_type.id).exists():
                        messages.error(request,'This package is already in the Sale.You can  change quantity ')
                        return redirect('sales:add_sales')  
                    saleproduct.cost_unit_price = saleproduct.package_type.selling_price
                    saleproduct.total_cost_price = saleproduct.quantity *  saleproduct.package_type.selling_price
                
                    if (saleproduct.quantity > saleproduct.package_type.available_quantity ):
                        messages.error(request, 'Can not sell quantity more than what is in stock ')
                        return redirect('sales:add_sales')
                else:
                    if sale.saleproduct_set.filter(product_id=product_id).exists():
                        messages.error(request,'This product is already in the Sale.You can  change quantity ')
                        return redirect('sales:add_sales')  
                    if (saleproduct.quantity > saleproduct.product.available_quantity ):
                        messages.error(request, 'Can not sell quantity more than what is in stock ')
                        return redirect('sales:add_sales')

            saleproduct.product = product
            saleproduct.calculate_total_cost_price()
            saleproduct.calculate_profit()
            
        

           
            if sale:
                sale=Sale.objects.get(pk=sale.id)
                saleproduct.sale = sale
                saleproduct.save()
                sale.save()

            
            if not sale:
                sale = Sale(creator=request.user)
                sale.save()
                request.session['active_sale'] = sale.pk
                saleproduct.sale = sale
                saleproduct.save()
                sale.save()
            messages.success(request,'product added successfully')
            return redirect('sales:add_sales')
        messages.error(request, str(form.errors))
        print(form.errors)
        return redirect('sales:add_sales')

   
   

        
@login_required(login_url='tenant:login')
def delete_sale_product(request, pk):
    product = SaleProduct.objects.get(pk=pk)
    sale=product.sale
    if product.sale and product.sale.saleproduct_set.count() <= 1:      
        if 'active_sale' in request.session:
            del request.session['active_sale']
            
            product.delete()
            sale.delete()
            messages.success(request,'product removed successfully')
            return redirect('sales:add_sales')
    else:
        product.delete()
        sale.save()
        messages.success(request,'product removed successfully')
        return redirect('sales:add_sales')

@login_required(login_url='tenant:login')
def update_quantity(request,pk):
    if request.method == "POST":
        quantity=request.POST['quantity']
        product = SaleProduct.objects.get(pk=pk)
        sale = product.sale
        product.quantity = int(quantity)
       
        product.save()
        product.calculate_total_cost_price()
        product.save()
        sale.save()
        messages.success(request,'product updated successfully')
        return redirect('sales:add_sales')
    
@login_required(login_url='tenant:login')
def add_discount(request):
    if request.method == 'POST':
        discount=request.POST['discountpercentage']
        sale = request.session.get('active_sale')
        if Sale.objects.filter(pk=sale).exists():
            sale_item = Sale.objects.get(pk=sale)
            sale_item.discount = Decimal(discount)
            sale_item.save()
            messages.success(request,'discount added successfully')
            return redirect('sales:add_sales')
        messages.error(request,'Can not discount ')
        return redirect('sales:add_sales')




@login_required(login_url='tenant:login')    
def create_tax(request):
    if request.method == 'POST':
        sale = request.session.get('active_sale')
        if Sale.objects.filter(pk=sale).exists():
            sale_item = Sale.objects.get(pk=sale)
            form = TaxForm(request.POST)
            if form.is_valid():
                tax = form.save()
                if tax.amount > sale_item.total_cost_price:
                    messages.error(request,"tax is greater than total amount")
                    return redirect('sales:add_sales')
                sale_item.tax.add(tax)
                sale_item.save()
                messages.success(request,'tax added successfully')
                return redirect('sales:add_sales')
            messages.error(request,str(form.errors))
            return redirect('sales:add_sales')
        messages.error(request,'Can not add tax ')
        return redirect('sales:add_sales')


@login_required(login_url='tenant:login')
def add_tax(request, pk):
    sale = request.session.get('active_sale')
    if Sale.objects.filter(pk=sale).exists():
        sale_item = Sale.objects.get(pk=sale)
        if sale_item.tax.filter(pk=pk).exists():
            messages.error(request,"tax already added")
            return redirect('sales:add_sales')

        tax = Tax.objects.get(id=pk)
        sale_item.tax.add(tax)
        sale_item.save()
        messages.success(request,f'{tax.name}  added')
        return redirect('sales:add_sales')
    messages.error(request,"can not add tax")
    return redirect('sales:add_sales')

@login_required(login_url='tenant:login')
def remove_tax(request, pk):
    sale = request.session.get('active_sale')
    if Sale.objects.filter(pk=sale).exists():
        sale_item = Sale.objects.get(pk=sale)
        tax = Tax.objects.get(id=pk)
        sale_item.tax.remove(tax)
        sale_item.save()
        messages.success(request,f'{tax.name}  removed ')
        return redirect('sales:add_sales')
    messages.success(request,"can not add tax")
    return redirect('sales:add_sales')



@login_required(login_url='tenant:login')
def add_payment(request):
    if request.method=="POST":
        sale = request.session.get('active_sale')
        if Sale.objects.filter(pk=sale).exists():
            sale_item = Sale.objects.get(pk=sale)
            paymentform = PaymentDetailsForm(request.POST)
            if paymentform.is_valid():
                payment = paymentform.save(commit=False)
                print(payment.balance)
                if payment.amount_paid <= 0:
                    messages.error(request,"amount paid can not be 0")
                    return redirect('sales:add_sales')
                elif payment.amount_paid < payment.balance:
                    messages.error(request,"amount paid can not be less the total cost price")
                    return redirect('sales:add_sales')
                else:
                    payment.save()
                    sale_item.payment = payment
                    sale_item.save()
                    messages.success(request,"payment added successfully")
                    return redirect('sales:add_sales')
            messages.error(request,str(paymentform.errors))
            return redirect('sales:add_sales')


                    
                    

        

@login_required(login_url='tenant:login')
def pause_sale(request):
    sale = request.session.get('active_sale')
    if Sale.objects.filter(pk=sale).exists():
            sale_item = Sale.objects.get(pk=sale)
            
            pausedsale = PausedSale.objects.create(sale=sale_item)
            pausedsale.save()
            if 'active_sale' in request.session:
             del request.session['active_sale']

             messages.success(request,"tansaction paused sucessfully")
             return redirect('sales:add_sales')
    messages.error(request,"can not pause sale")
    return redirect('sales:add_sales')


@login_required(login_url='tenant:login')
def showpausedsale(request):
    context = {
        "sales": PausedSale.objects.all(),
        
    }
    return render(request,"sales/pausedsales.html",context=context)


@login_required(login_url='tenant:login')
def resume_sale(request, pk):
    if Sale.objects.filter(pk=pk).exists():
            request.session['active_sale'] = pk
            return redirect('sales:add_sales')


@login_required(login_url='tenant:login')    
def complete_sale(request):
    if request.method == 'POST':



        sale = request.session.get('active_sale')
        if Sale.objects.filter(pk=sale).exists():
        
            
                sale_item = Sale.objects.get(pk=sale)
                form = SaleForm(request.POST, instance=sale_item)
                if form.is_valid():
                        form.save(commit=True)
            
               
                if sale_item.payment:

                    for item in sale_item.saleproduct_set.all():
                        if item.package_type:
                            product = item.package_type
                            product.available_quantity = product.available_quantity - item.quantity
                        else:
                            product = item.product
                            product.available_quantity = product.available_quantity - item.quantity


                        product.save()
                    sale_item.status = "completed"
                    
                    sale_item.save()
                    



                    
                    setting = AppSettings.objects.first()
                    
                    if setting.automatic_print_receipt:
                            del request.session['active_sale']
                            sale = Sale.objects.get(id=sale)
                            template = get_template('sales/receipt.html')  # Replace with your actual template name
                            html_content = template.render({
                                'sale': sale,
                                "pharmacy": get_tenant(request),
                                'user': request.user,
                                'saleproducts': SaleProduct.objects.filter(sale=sale.id).order_by("-id"),
                            
                            })  # Replace with your actual data

                            options = {
                               'page-width': "3.875in",
                                'page-height':"7.5in",
                            
                                    'encoding': 'UTF-8',   
                                'margin-top': '0in',
                                'margin-right': '0in',
                                'margin-bottom': '0in',
                                'margin-left': '0in',
                            }

                            config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
                            pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

                            response = HttpResponse(pdf_data, content_type='application/pdf')
                            response['Content-Disposition'] = 'inline; filename="preview.pdf"'
                            return response

                    else:
                        messages.success(request,"sale completed")
                        return redirect('sales:add_sales')
                messages.error(request,"Add Payment")
                return redirect('sales:add_sales')
        return redirect('sales:add_sales')
   

@login_required(login_url='tenant:login')
def view_sale_details(request, pk):
    sale_item = Sale.objects.get(pk=pk)
    context = {
        "sale": sale_item,
        'saleproducts': SaleProduct.objects.filter(sale=sale_item).order_by("-id"),
    }
    return render(request,"sales/saledetails.html",context=context)


@login_required(login_url='tenant:login')
def receipt(request, pk):
    if 'active_sale' in request.session:
        del request.session['active_sale']
    sale = Sale.objects.get(id=pk)
    template = get_template('sales/receipt.html')  # Replace with your actual template name
    html_content = template.render({
        'sale': sale,
        "pharmacy": get_tenant(request),
        'user': request.user,
        
        'saleproducts': SaleProduct.objects.filter(sale=sale).order_by("-id"),
    
    })  # Replace with your actual data

    options = {
       
     'page-width': "3.875in",
     'page-height':"7.5in",
   
        'encoding': 'UTF-8',   
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
  
    }

    config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdf_data = pdfkit.from_string(html_content, False, configuration=config, options=options)

    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="preview.pdf"'
    return response

@login_required(login_url='tenant:login')
def delete_sale(request):
    if  Sale.objects.filter(pk=request.session.get('active_sale')).exists():
        sale= Sale.objects.get(pk=request.session.get('active_sale'))
        del request.session['active_sale']
        sale.saleproduct_set.all().delete()
        sale.delete()
    return redirect('sales:add_sales')


