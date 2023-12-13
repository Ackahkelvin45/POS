from django.urls import path
from . import views
from .views import GetAvailableQuantityView

app_name = "inventory"

urlpatterns = [
    path('add/', views.showaddstock, name="add_inventory"),
    path('correct/', views.showchangestock, name="change_inventory"),
    path('get_available_quantity/', GetAvailableQuantityView.as_view(), name='get_available_quantity'),
    path('history/', views.stockEntryList, name="history"),
    path('add_process/', views.add_stock_process, name="add_inventory_process"),
    path('change_process/', views.change_stock_process, name="change_inventory_process"),


    
]