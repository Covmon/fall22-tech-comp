from django.urls import path, include
from account.views import *
from django.contrib.auth import views as auth_views
from account.forms import LoginForm

urlpatterns = [
    path("@<url_username>", account_detail, name="account_detail"),
    path("api/staff-profile/<url_username>/", account_detail, name="account_detail"),
    path("account/settings/", account_settings, name="account_settings"),
    path("", include('django.contrib.auth.urls')),
    path("login/", auth_views.LoginView.as_view(form_class=LoginForm)),
]