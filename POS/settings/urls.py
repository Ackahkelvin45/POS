from django.urls import path
from . import views


app_name = "settings"

urlpatterns = [
    
    path("email/", views.showEmailSettings, name="emailsettings"),
    path("sale/", views.showSalesSettings, name="salessettings"),
    path("email_setup_process/", views.add_email_process, name="email_setup_process"),
    path("change/", views.change_settings, name="change_settings"),
    
]