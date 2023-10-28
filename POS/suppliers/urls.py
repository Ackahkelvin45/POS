from django.urls import path
from . import views


app_name = "suppliers"

urlpatterns=[

path("add/", views.showAddSuppliers, name='add_supplier'),
path("add_process/",views.addSuppliersProcess,name='add_supplier_process'),
]