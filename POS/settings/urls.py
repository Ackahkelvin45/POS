from django.urls import path
from . import views


app_name = "settings"

urlpatterns = [
    
    path("email/", views.showEmailSettings, name="emailsettings"),
    path("email/edit/<int:pk>/", views.editEmailSettings, name="editemailsettings"),
    path("sale/", views.showSalesSettings, name="salessettings"),
    path("general/", views.showGeneralSettings, name="generalsettings"),
    path("email_setup_process/", views.add_email_process, name="email_setup_process"),
    path("email_edit_process/", views.edit_email_process, name="email_edit_process"),
    path("change/", views.change_settings, name="change_settings"),
     path("change_general/", views.change_general_settings, name="change_general_settings"),
    
]