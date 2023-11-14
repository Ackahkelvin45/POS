from django.urls import path
from . import views


app_name = "suppliers"

urlpatterns = [
    path("add/", views.showAddSuppliers, name="add_supplier"),
    path("add_process/", views.addSuppliersProcess, name="add_supplier_process"),
    path("list/", views.supplierslist, name="suppliers_list"),
        path('export-suppliers-pdf/', views.export_suppliers_as_pdf, name='export_suppliers_as_pdf'),

<<<<<<< HEAD
]
=======
path("add/", views.showAddSuppliers, name='add_supplier'),
path("edit/<int:pk>/", views.edit_supplier, name='edit_supplier'),
path("edit_process/<int:pk>/", views.edit_supplier_process, name='edit_supplier_process'),
path("add_process/",views.addSuppliersProcess,name='add_supplier_process'),
path('list/', views.supplierslist, name="supplierlist"),
path('delete/<int:pk>/',views.delete_supplier,name='deletesupplier')
]
>>>>>>> 4c06f3e6412e08eb08a5f31a74fb0b63f4e12c52
