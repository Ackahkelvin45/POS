from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("add_category/", views.showAddCategory, name="categorypage"),
    path("category_list/", views.showCategoryList, name="categorylist"),
    path("subcategory_list/", views.showSubCategoryList, name="subcategorylist"),
    path("add_sub_category/", views.showAddSubCategory, name="subcategorypage"),
    path("add_product/", views.showAddProduct, name="productpage"),
    path("add_product_process/", views.addProductProcess, name="addProduct"),
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
    ),  # changed from subcategory_process to subcategory_list
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
]
