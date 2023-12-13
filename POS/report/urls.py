from django.urls import path
from . import views

app_name = "report"


urlpatterns = [
    path("daily/",views.daily_report,name="daily_report",)
    
]