from django.shortcuts import render
from sales.models import Sale
from django.db.models import Sum

# Create your views here.

def daily_report(request):
    context = {
        "sales": Sale.objects.filter(status="completed"),
     "total_cost_price": Sale.objects.filter(status='completed').aggregate(total_cost_price_sum=Sum('total_cost_price'))['total_cost_price_sum'],
     "total_number":Sale.objects.filter(status='completed').count()
    }
    return render(request,"report/dailyreport.html",context=context)

