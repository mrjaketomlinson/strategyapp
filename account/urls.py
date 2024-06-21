from django.urls import path

from account import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/login/", views.UserLogin.as_view(), name="login")
]