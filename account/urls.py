from django.urls import path

from account import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/organization-signup/", views.organization_create, name="organization_create"),
    path("accounts/login/", views.UserLogin.as_view(), name="login"),
    path("accounts/admin/", views.admin, name="admin"),
    path("accounts/user/all/", views.user_all, name="user_all"),
    path("accounts/team/all/", views.team_all, name="team_all"),
    path("accounts/team/create/", views.team_create, name="team_create"),
    path("accounts/team/<int:team_id>/", views.team_detail, name="team_detail"),
    path("accounts/team/<int:team_id>/edit/", views.team_edit, name="team_edit"),
    path("accounts/team/<int:team_id>/delete/", views.team_delete, name="team_delete"),
    path("accounts/team/<int:team_id>/member/create/", views.team_member_create, name="team_member_create"),
    path("accounts/team/<int:team_id>/member/<int:user_id>/edit/", views.team_member_edit, name="team_member_edit"),
    path("accounts/team/<int:team_id>/member/<int:user_id>/delete/", views.team_member_delete, name="team_member_delete"),
    path("accounts/period/all/", views.time_period_all, name="time_period_all"),
    path("accounts/period/create/", views.time_period_create, name="time_period_create"),
    path("accounts/period/<int:time_period_id>/edit/", views.time_period_edit, name="time_period_edit"),
    path("accounts/period/<int:time_period_id>/", views.time_period_detail, name="time_period_detail"),
]