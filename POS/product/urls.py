from django.urls import path
from . import views
from django_pdfkit import PDFView


app_name = "product"

urlpatterns = [
    path("add_category/", views.showAddCategory, name="categorypage"),
    path("category_list/", views.showCategoryList, name="categorylist"),
    path("subcategory_list/", views.showSubCategoryList, name="subcategorylist"),
    path("add_sub_category/", views.showAddSubCategory, name="subcategorypage"),
    path("add/", views.showAddProduct, name="productpage"),
     path("edit/<int:pk>/", views.editProduct, name="editproduct"),
    path("list/", views.showProducts, name="productlist"),
    path("add_product_process/<int:pk>/", views.edit_product_process, name="edit_product_process"),
    path("add_product_process/", views.addProductProcess, name="addProduct"),
     path("delete_product/<int:pk>/", views.delete_product, name="delete_product"),
    path("add_unit/", views.showAddUnit, name="unitpage"),
    path("unit_list/", views.showUnitList, name="unitlist"),
    path("add_unit_process/", views.add_unit_process, name="add_unit"),
    path("edit_unit/<int:pk>/", views.edit_unit, name="edit_unit"),
    path(
        "edit_unit_process/<int:pk>/", views.edit_unit_process, name="edit_unit_process"
    ),
    path("delete_unit/<int:pk>/", views.delete_unit, name="delete_unit"),
    path("add_subcategory_process/", views.add_subcategory, name="subcategory_process"),
    path(
        "subcategory_list/", views.showSubCategoryList, name="subcategory_list"
    ),
    
    # changed from subcategory_process to subcategory_list
    path("edit_subcategory/<int:pk>/", views.edit_subcategory, name="edit_subcategory"),
    path(
        "edit_subcategory_process/<int:pk>/",
        views.edit_subcategory_process,
        name="edit_subcategory_process",
    ),
    path(
        "delete_subcategory/<int:pk>/",
        views.delete_subcategory,
        name="delete_subcategory",
    ),
    path("add_category_process/", views.add_category, name="category_process"),
    path("edit_category/<int:pk>/", views.edit_category, name="edit_category"),
    path(
        "edit_category_process/<int:pk>/",
        views.edit_category_process,
        name="edit_category_process",
    ),
    path("delete_category/<int:pk>/", views.delete_category, name="delete_category"),
    path(
        "create_category_from_excel/",
        views.create_categories_from_excel,
        name="create_category_from_excel",
    ),
    path(
        "create_subcategory_from_excel/",
        views.create_subcategories_from_excel,
        name="create_subcategory_from_excel",
    ),
    path(
        "create_unit_from_excel/",
        views.create_units_from_excel,
        name="create_unit_from_excel",
    ),

    path('add_package/', views.showAddPackage, name='add_package'),
    path('add_package_process/', views.addPackage, name='add_package_process'),
    path('export-products-pdf/', views.export_products_as_pdf, name='export_products_as_pdf'),
     path('export-package-pdf/', views.export_packages_as_pdf, name='export_packages_as_pdf'),
    path('export-categories-pdf/', views.export_categories_as_pdf, name='export_categories_as_pdf'),
    path('export-subcategories-pdf/', views.export_subcategories_as_pdf, name='export_subcategories_as_pdf'),
    path('export-units-pdf/', views.export_units_as_pdf, name='export_units_as_pdf'),
    path('export_products/excel/', views.export_products_to_excel, name='export_products_to_excel'),
        path('export_package/excel/', views.export_package_to_excel, name='export_package_to_excel'), 
    path('export_categories/excel/', views.export_categories_to_excel, name='export_categories_to_excel'),
     path('export_subcategories/excel/', views.export_subcategories_to_excel, name='export_dubcategories_to_excel'),
          path('export_units/excel/', views.export_units_to_excel, name='export_units_to_excel'),    
    path('reset_products_to_zero/', views.reset_product_to_zero, name='reset_product_to_zero'),
    path('reset_package_to_zero/', views.reset_package_to_zero, name='reset_package_to_zero'),
    path('delete_all_category/', views.delete_all_categories, name='delete_all_categories'),
    path('delete_all_subcategory/', views.delete_all_subcategories, name='delete_all_subcategories'),
    path('delete_all_units/', views.delete_all_units, name='delete_all_units'),
     path('update_quantity_in_bulk/', views.update_quantity_in_bulk, name='update_quantity_in_bulk'),

      path('update_package_quantity_in_bulk/', views.update_packages_quantity_in_bulk, name='update_package_quantity_in_bulk'),
    



]
