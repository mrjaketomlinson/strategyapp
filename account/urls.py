from django.urls import path

from account import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/organization-signup/", views.organization_create, name="organization_create"),
    path("accounts/login/", views.UserLogin.as_view(), name="login"),
    path("team/all/", views.team_all, name="team_all"),
    path("team/create/", views.team_create, name="team_create"),
    path("team/<int:team_id>/", views.team_detail, name="team_detail"),
]