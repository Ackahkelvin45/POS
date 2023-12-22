from django.urls import path
from . import views

app_name = "report"


urlpatterns = [
    path("daily/", views.daily_report, name="daily_report",),
     path("inventory/",views.inventoryreport,name="inventoryreport"),
     path("date/", views.showdatepicker, name="datepicker"),
     path("get_products/", views.getproducts, name="getproducts"),
     path("get_packages/",views.getpackages,name="getpackages"),
    
]