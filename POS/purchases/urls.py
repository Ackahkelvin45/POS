from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('order/', views.showOrderPage, name='order'),
    path('search_product/', views.search_product, name='search_product'),
    path('order/<int:pk>', views.order_item, name='order_item'),
    path("purchase_item/", views.purchase_item, name='purchase_item'),
    path("remove_item/<int:pk>/", views.delete_ordered_product, name="remove"),
    path("edit_item/<int:pk>/", views.edit_item, name="edit_item"),
    path("edit_item_process/<int:pk>/", views.edit_item_process, name="edit_item_process"),
    path("save_purchase_order/", views.save_purchase_order, name="save_purchase_order"),
    path("preview/", views.preview_as_pdf, name="preview_as_pdf"),
     path("preview/<int:pk>/", views.preview_as_pdf2, name="preview_as_pdf2"),
    path("delete/", views.delete_purchaseorder, name="delete_purchaseorder"),
    path("list/", views.view_purchase_order_list, name="purchaseorderlist"),
    path("edit/<int:pk>/", views.edit_purchase_order, name="editpurchaseorder"),
     path("delete/<int:pk>/", views.delete_purchaseorder2, name="delete_purchaseorder2"),
     path("recieve/<int:pk>/", views.recieve_order, name="recieve_order"),
     path("recieve_process/<int:pk>/", views.receive_stock_process, name="recieve_order_process"),
]