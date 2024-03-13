from django.urls import path
from . import views



app_name = "auth"


urlpatterns = [
    path("", views.showSignuppage, name="signup"),
    path("show/", views.show, name="signupss"),
    path("signup_process/", views.signupprocess, name="signup_process"),
    path("preview/", views.preview_template, name="preview"),
]
