from django.urls import path


from django.contrib.auth import views as auth_views



urlpatterns=[
    path("reset_password/",
    auth_views.PasswordResetView.as_view(template_name='accounts/resetpassword.html'),
    name='password_reset'),
    path("reset_password_sent/",
    auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
    name="password_reset_done"),
    path("reset/<uidb64>/<token>/"
    , auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/",
     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset_complete.html"), name="password_reset_complete"),
]