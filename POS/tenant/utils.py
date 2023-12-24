from datetime import timedelta
from django.utils import timezone
from sales.models import Sale,SaleProduct
from django.db.models.functions import TruncMonth,TruncYear, TruncDay,TruncWeek,Coalesce
from calendar import monthrange
from django.db.models import Sum, Count, F



def calculate_sales_percentage():
    # Get the current time
    now = timezone.now()

    # Calculate the start time for the past 48 hours
    forty_eight_hours_ago = now - timedelta(hours=48)

    # Calculate the start time for the past 24 hours
    twenty_four_hours_ago = now - timedelta(hours=24)

    # Get sales in the past 48 hours
    total_sales_past_48_hours = Sale.objects.filter(
        status="completed",
        date_created__range=(forty_eight_hours_ago, twenty_four_hours_ago)
    ).aggregate(total_cost_price=Sum('total_cost_price'))

    # Get the sum of total cost price of sales in the past 24 hours
    total_cost_price_past_24_hours = Sale.objects.filter(
        status="completed",
        date_created__gte=twenty_four_hours_ago
    ).aggregate(total_cost_price=Sum('total_cost_price'))

    # Extract the total sales and total cost price values
    total_sales_value = total_sales_past_48_hours['total_cost_price'] or 0
    total_cost_price_value = total_cost_price_past_24_hours['total_cost_price'] or 0

    # Calculate the percentage change
    percentage_change = ((total_cost_price_value- total_sales_value ) / total_sales_value) * 100 if total_sales_value != 0 else 0

    # Return the results
    return {
        'total_sales': total_sales_value,
        'total_cost_price_24': total_cost_price_value,
        'percentage_change': percentage_change
    }



def calculate_sales_number():
    # Get the current time
    now = timezone.now()

    # Calculate the start time for the past 48 hours
    forty_eight_hours_ago = now - timedelta(hours=48)

    # Calculate the start time for the past 24 hours
    twenty_four_hours_ago = now - timedelta(hours=24)

    # Get sales in the past 48 hours
    total_sales_past_48_hours = Sale.objects.filter(
        status="completed",
        date_created__range=(forty_eight_hours_ago, twenty_four_hours_ago)
    ).count()

    # Get the sum of total cost price of sales in the past 24 hours
    total_sales_past_24_hours = Sale.objects.filter(
        status="completed",
        date_created__gte=twenty_four_hours_ago
    ).count()



    # Calculate the percentage change
    percentage_change = ((total_sales_past_24_hours- total_sales_past_48_hours ) / total_sales_past_48_hours) * 100 if total_sales_past_48_hours != 0 else 0

    # Return the results
    return {
        'total_quantity':total_sales_past_24_hours ,
       
        'percentage_change': percentage_change
    }







def calculate_gross_proft_percentage():
    # Get the current time
    now = timezone.now()

    # Calculate the start time for the past 48 hours
    forty_eight_hours_ago = now - timedelta(hours=48)

    # Calculate the start time for the past 24 hours
    twenty_four_hours_ago = now - timedelta(hours=24)

    # Get sales in the past 48 hours
    total_sales_past_48_hours = Sale.objects.filter(
        status="completed",
        date_created__range=(forty_eight_hours_ago, twenty_four_hours_ago)
    ).aggregate(total_gross_profit=Sum('total_gross_profit'))

    # Get the sum of total cost price of sales in the past 24 hours
    total_cost_price_past_24_hours = Sale.objects.filter(
        status="completed",
        date_created__gte=twenty_four_hours_ago
    ).aggregate(total_gross_profit=Sum('total_gross_profit'))

    # Extract the total sales and total cost price values
    total_profit_value_in_48 = total_sales_past_48_hours['total_gross_profit'] or 0
    total_cost_price_value_24 = total_cost_price_past_24_hours['total_gross_profit'] or 0

    # Calculate the percentage change
    percentage_change = ((total_cost_price_value_24- total_profit_value_in_48 ) / total_profit_value_in_48) * 100 if total_profit_value_in_48!= 0 else 0

    # Return the results
    return {
        'total_profit': total_profit_value_in_48,
        'total_profit_price_24': total_cost_price_value_24,
        'percentage_change': percentage_change
    }







def get_sales_by_all_months_in_year():
    current_year = timezone.now().year

    return (
        Sale.objects
        .exclude(date_created__isnull=True)
        .filter(date_created__year=current_year)
        .annotate(month=TruncMonth('date_created'))
        .values('month')
        .annotate(
            total_cost_price=Sum('total_cost_price'),
            total_gross_profit=Sum('total_gross_profit'),
        )
        .order_by('month')
    )


def get_sales_by_current_week():
   
    current_date = timezone.now()

    # Calculate the start and end of the current week
    start_of_week = current_date - timezone.timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    return (
        Sale.objects
        .exclude(date_created__isnull=True)
        .filter(date_created__range=(start_of_week, end_of_week))
        .annotate(day=TruncDay('date_created'))
        .values('day')
        .annotate(
            total_cost_price=Sum('total_cost_price'),
            total_gross_profit=Sum('total_gross_profit'),
        )
        .annotate(formatted_day=F('day'))  
        .order_by('day')
    )


def get_top_products():
    now = timezone.now()


    # Calculate the start time for the past 24 hours
    twenty_four_hours_ago = now - timedelta(hours=24)
    
    return( SaleProduct.objects.filter(
    sale__status='completed',
    sale__date_created__range=( twenty_four_hours_ago , now)
        )
        .values('product__name','product__product_image') \
        .annotate(total_quantity_sold=Coalesce(Sum('quantity'), 0)) \
        .order_by('-total_quantity_sold')[:5]
    )


def get_top_products_all():
    now = timezone.now()


    # Calculate the start time for the past 24 hours
    twenty_four_hours_ago = now - timedelta(hours=24)
    
    return( SaleProduct.objects.filter(
    sale__status='completed',
    sale__date_created__range=( twenty_four_hours_ago , now)
        )
        .values('product__name','product__product_image') \
        .annotate(total_quantity_sold=Coalesce(Sum('quantity'), 0)) \
        .order_by('-total_quantity_sold')[:10]
    )



def calculate_sales_percentage_input(start_date=None, end_date=None):
    # Set default values if start_date and end_date are not provided
 

    # Get sales in the specified date range
    total_sales_number = Sale.objects.filter(
        status="completed",
        date_created__range=(start_date, end_date)
    ).count()


    total_cost_price = Sale.objects.filter(
        status="completed",
         date_created__range=(start_date, end_date)
    ).aggregate(total_cost_price=Sum('total_cost_price'))
    total_gross_profit= Sale.objects.filter(
        status="completed",
         date_created__range=(start_date, end_date)
    ).aggregate(total_gross_profit=Sum('total_gross_profit'))

    top_products_10= SaleProduct.objects.filter(
    sale__status='completed',
    sale__date_created__range=( start_date , end_date)
        ).values('product__name', 'product__product_image') \
        .annotate(total_quantity_sold=Coalesce(Sum('quantity'), 0)) \
        .order_by('-total_quantity_sold')[:10]
    sales= Sale.objects.filter(
        status="completed",
         date_created__range=(start_date, end_date)
    )
    
   
        


    return {
        'total_sales_number': total_sales_number,
        'total_cost_price': total_cost_price,
         'total_gross_profit': total_gross_profit,
        'top_products_10': top_products_10,
        'sales':sales
            }