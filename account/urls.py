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
    path("team/<int:team_id>/edit/", views.team_edit, name="team_edit"),
    path("team/<int:team_id>/delete/", views.team_delete, name="team_delete"),
    path("team/<int:team_id>/member/create/", views.team_member_create, name="team_member_create"),
    path("team/<int:team_id>/member/<int:user_id>/delete/", views.team_member_delete, name="team_member_delete"),
]