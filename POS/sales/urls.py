from django.urls import path
from . import views  

app_name = "sales"

urlpatterns = [
    path("add/", views.show_add_sales, name="add_sales"),
    path("history/", views.show_sales_history, name="sales_history"),
    path('search_product/', views.search_product, name='search_product'),
    path('sell/<int:pk>/', views.order_item, name='order_item'),
    path("sell/",views.sell_item,name="sell_item"),
    path("delete/<int:pk>/", views.delete_sale_product, name="delete_item"),
    path("update/<int:pk>/", views.update_quantity, name="update_quantity"),
    path("add_discount/", views.add_discount, name="add_discount"),
    path("create_tax/", views.create_tax, name="create_tax"),
    path("add_tax/<int:pk>/", views.add_tax, name="add_tax"),
    path("remove_tax/<int:pk>/", views.remove_tax, name="remove_tax"),
    path("add_payment/", views.add_payment, name="add_payment"),
    path("pause_sale/", views.pause_sale, name="pause_sale"),
    path("paused-sales/", views.showpausedsale, name="paused_sales"), 
    path("resume_sale/<int:pk>/", views.resume_sale, name="resume_sale"),
    path("complete_sale/", views.complete_sale, name="complete_sale"),
    path("details/<int:pk>/", views.view_sale_details, name="sale_detail"),
    path("receipt/<int:pk>/", views.receipt, name="receipt"),
    path("delete_all/",views.delete_sale,name='delete_sale')

]