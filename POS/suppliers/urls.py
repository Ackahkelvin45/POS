from django.urls import path
from . import views


app_name = "suppliers"

urlpatterns = [
    path("add/", views.showAddSuppliers, name="add_supplier"),
    path("add_process/", views.addSuppliersProcess, name="add_supplier_process"),
    path("list/", views.supplierslist, name="suppliers_list"),
        path('export-suppliers-pdf/', views.export_suppliers_as_pdf, name='export_suppliers_as_pdf'),

]
