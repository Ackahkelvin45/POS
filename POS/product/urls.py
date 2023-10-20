from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('add_category/', views.showAddCategory, name='categorypage'),
    path('add_sub_category/', views.showAddSubCategory, name='subcategorypage'),
    path('add_product/', views.showAddProduct, name='productpage'),
    path('add_unit/', views.showAddUnit, name='unitpage'),
    path('add_subcategory_process/', views.add_subcategory, name='subcategory_process'),
   
    
]