from django.urls import path
from . import views


app_name = "suppliers"

urlpatterns=[

path("add/", views.showAddSuppliers, name='add_supplier'),
path("edit/<int:pk>/", views.edit_supplier, name='edit_supplier'),
path("edit_process/<int:pk>/", views.edit_supplier_process, name='edit_supplier_process'),
path("add_process/",views.addSuppliersProcess,name='add_supplier_process'),
path('list/', views.supplierslist, name="supplierlist"),
path('delete/<int:pk>/',views.delete_supplier,name='deletesupplier')
]