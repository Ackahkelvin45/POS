from django.shortcuts import render,redirect
from django_tenants.utils import get_tenant
from main.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sales.models import Sale
from django.db.models import Sum
from django.utils import timezone
from product.models import Product_Item, Package
from datetime import datetime, timedelta
from .utils import calculate_sales_percentage,calculate_sales_number,calculate_gross_proft_percentage,get_sales_by_all_months_in_year,get_sales_by_current_week,get_top_products,calculate_sales_percentage_input

# Create your views here.


      
@login_required(login_url='tenant:login')
def viewDashboard(request):
        now = timezone.now()
        twenty_four_hours_ago = now - timezone.timedelta(hours=24)
        daily_sales=Sale.objects.filter(status="completed",date_created__gte=twenty_four_hours_ago)  
        tenant = get_tenant(request)       
        user = request.user
        pharmacy_name = tenant.name
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

        sales_by_month = get_sales_by_all_months_in_year()
        sales_by_week = get_sales_by_current_week()
        top_products_in_24 = get_top_products()
        print(top_products_in_24)
      
  


      
        context = {
                    "pharmacy_name": pharmacy_name,
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
                    "daily_sales": daily_sales,
                    'sales_by_month': sales_by_month,
                    'sales_by_week': sales_by_week,
                    "top_5_products_in_24_hours":top_products_in_24
                    
                      
                   
                }

        return render(request, 'tenant/dashboard.html', context=context)


def showLoginpage(request):
    return render(request, 'tenant/login.html')



def login_process(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        user=authenticate(email=email, password=password)
        print(user)     
        if user is not None:            
                login(request,user)                             
                return redirect("tenant:dashboard")
        else:
            messages.error(request,'Incorrect username or password. Please try again.')
            return redirect("tenant:login")
                


def logout_user(request):
    logout(request)
    return redirect("tenant:login")

    