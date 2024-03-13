from django.urls import path
from . import views
from django.contrib.auth  import views as auth_views 

app_name = "tenant"

urlpatterns = [
  
    path("", views.viewDashboard, name='dashboard'),
    path("login/", views.showLoginpage, name='login'),
    path("login_process/", views.login_process, name="login_process"),
    path("logout_process/",views.logout_user,name="logout"),

]