from django.shortcuts import render
from sales.models import Sale
from django.db.models import Sum
from django.utils import timezone
from product.models import Product_Item, Package
from tenant.utils import calculate_sales_percentage,calculate_sales_number,calculate_gross_proft_percentage,get_top_products_all

# Create your views here.

def daily_report(request):
    now = timezone.now()
    twenty_four_hours_ago = now - timezone.timedelta(hours=24)
    sales = Sale.objects.filter(status="completed", date_created__gte=twenty_four_hours_ago)
    sales_total_price = calculate_sales_percentage()
    sales_total_amount = calculate_sales_number()
    sales_total_profit=calculate_gross_proft_percentage()



    increasedsales = False
    salessame = False
    salesdecrease=False
    if sales_total_price['percentage_change'] > 0:
            increasedsales=True
    elif sales_total_price['percentage_change'] < 0:
              salesdecrease=True
    else:
             salessame=True
            
    increasedamount = False
    amountsame = False
    amountdecrease=False
    if sales_total_amount['percentage_change']> 0:
            increasedamount=True
    elif sales_total_amount['percentage_change'] < 0:
              amountdecrease=True
    else:
             amountsame=True
            
    increasedprofit = False
    profitsame = False
    profitdecrease = False
 
    if sales_total_profit['percentage_change'] > 0:
           increasedprofit=True
    elif sales_total_profit['percentage_change'] < 0:
              profitdecrease=True
    else:
             profitsame = True

    top_products_in_24 = get_top_products_all()
   
      
  


    context = {
    "daily_sales":sales ,
    "total_cost_price": sales.aggregate(total_cost_price_sum=Sum('total_cost_price'))['total_cost_price_sum'],
    "total_number": sales.count(),
    "daily_total_cost_price": sales_total_price['total_cost_price_24'],
    "daily_sales_amount": sales_total_amount['total_quantity'],
    "daily_profit": sales_total_profit['total_profit_price_24'],
    "percentage_change_in_amount":round(sales_total_amount['percentage_change'],1),
    'percentage_change_in_sales': round(sales_total_price['percentage_change'], 1),
    'percentage_change_in_profit':  round(sales_total_profit['percentage_change'], 1),
    "salesincrease": increasedsales,
    'salessame': salessame,
    "salesdecrease": salesdecrease,
    "increasedamount": increasedamount,
    'amountsame': amountsame,
    "amountdecrease": amountdecrease,
    "increasedprofit": increasedprofit,
    'profitsame': profitsame,
    "profitdecrease": profitdecrease,
    "top_products_10_in_24_hours":top_products_in_24
                         
    }
    return render(request,"report/dailyreport.html",context=context)


def inventoryreport(request):
    context = {
        "products": Product_Item.objects.all(),
        "packages":Package.objects.all(),
    }
    return render(request, "report/inventoryreport.html", context=context)
    


def showdatepicker(request):
    return render(request, "report/datepicker.html")
   


def getproducts(request):
    if request.method == 'POST':
        checked_products = request.POST.getlist('product')
       
        selected_products = Product_Item.objects.filter(pk__in=checked_products)
        context = {
            'products':selected_products
        }
        return render (request,"report/productreport.html",context=context)

def getpackages(request):
    if request.method == 'POST':
        checked_products = request.POST.getlist('package')
        print(checked_products)
       
        selected_products = Package.objects.filter(pk__in=checked_products)
        context = {
            'products':selected_products
        }
        return render (request,"report/productreport.html",context=context)
