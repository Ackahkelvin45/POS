from django.shortcuts import render,redirect 
from .forms import StockEntryForm
from django.views import View
from product.models import Product_Item
from django.http import JsonResponse
from django.contrib import messages
from .models import StockEntry

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
        product_id = request.GET.get('product_id')
        product = Product_Item.objects.get(pk=product_id)
        available_quantity = product.available_quantity  # Replace 'available_quantity' with your actual field name

        return JsonResponse({'available_quantity': available_quantity})


def add_stock_process(request):
    if request.method == "POST":
        stockentryform = StockEntryForm(request.POST)
        if stockentryform.is_valid():
            stock = stockentryform.save()
            product = stock.product
            stock.previous_quantity=product.available_quantity
            stock.add_to_stock()
            stock.info = f"{stock.product.name} updated by {stock.quantity_received} manually"
            stock.user = request.user
            stock.available_quantity=stock.product.available_quantity
            stock.save()

            messages.success(request,'Inventory added succesfully')
            return redirect('inventory:history')

def change_stock_process(request):
    if request.method == "POST":
        stockentryform = StockEntryForm(request.POST)
        if stockentryform.is_valid():
            stock = stockentryform.save()
            product = stock.product
            stock.previous_quantity=product.available_quantity
            stock.change_stock()
            stock.info = f"{stock.product.name} changed  to  {stock.quantity_received} manually"
            stock.user = request.user
            stock.available_quantity=stock.product.available_quantity
            stock.save()

            messages.success(request,'Inventory Corrected  succesfully')
            return redirect('inventory:history')

def stockEntryList(request):
    context = {
        "stockentry":StockEntry.objects.all().order_by('-id'),
    }
    return render(request,'stock/stockhistorylist.html',context=context)