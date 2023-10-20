from django.urls import path,include
from . import views
from django.contrib import admin


app_name = 'main'

urlpatterns = [

 path('admin/', admin.site.urls),
 path("__reload__/", include("django_browser_reload.urls")),
 path("",include("authentication.urls")),


    
]


