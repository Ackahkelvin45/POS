from django.shortcuts import render,redirect 
from .forms import StockEntryForm
from django.views import View
from product.models import Product_Item
from django.http import JsonResponse
from django.contrib import messages
from .models import StockEntry
from product.models import Package

# Create your views here.

def showaddstock(request):
    context = {
        "stockform":StockEntryForm()
    }
    return render(request, "stock/addstock.html", context=context)
    

def showchangestock(request):
    context = {
        "stockform":StockEntryForm()
    }
    return render(request, "stock/stockcorrection.html", context=context)
    
class GetAvailableQuantityView(View):
    def get(self, request, *args, **kwargs):
        try:
            product_id = request.GET.get('product_id')
            product = Product_Item.objects.get(pk=product_id)
            available_quantity = product.available_quantity
            packages = Package.objects.filter(product__id=product_id).values('id', 'package_name')

            return JsonResponse({'available_quantity': available_quantity, "packages": list(packages)})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class GetAvailablePackageQuantityView(View):
    def get(self, request, *args, **kwargs):
        try:
            package_id = request.GET.get('package_id')
            package = Package.objects.get(pk=package_id)
            available_quantity = package.available_quantity

            
            return JsonResponse({'available_quantity': available_quantity})


        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def add_stock_process(request):
    if request.method == "POST":
        stockentryform = StockEntryForm(request.POST)
        if stockentryform.is_valid():
            stock = stockentryform.save()
            if stock.package_type:
                product = stock.package_type
                stock.previous_quantity = product.available_quantity
                stock.add_to_stock()
                stock.available_quantity=stock.package_type.available_quantity
            else:
                product = stock.product
                stock.previous_quantity = product.available_quantity
                stock.add_to_stock()
                stock.available_quantity=stock.product.available_quantity
            
            stock.user = request.user
            stock.save()

            messages.success(request,'Inventory added succesfully')
            return redirect('inventory:history')

def change_stock_process(request):
    if request.method == "POST":
        stockentryform = StockEntryForm(request.POST)
        if stockentryform.is_valid():
            stock = stockentryform.save()
            if stock.package_type:
                product = stock.package_type
                stock.previous_quantity = product.available_quantity
                stock.change_stock()
                stock.available_quantity = stock.package_type.available_quantity
                
            else:
                product = stock.product
                
                stock.previous_quantity = product.available_quantity
                stock.change_stock()
                stock.available_quantity=stock.product.available_quantity        
                
            stock.user = request.user
            
            stock.save()

            messages.success(request,'Inventory Corrected  succesfully')
            return redirect('inventory:history')

def stockEntryList(request):
    context = {
        "stockentry":StockEntry.objects.all().order_by('-id'),
    }
    return render(request,'stock/stockhistorylist.html',context=context)