from django.urls import path

from strategy import views

urlpatterns = [
    path("accounts/criterion/all/", views.criterion_all, name="criterion_all"),
    path("accounts/criterion/create/", views.criterion_create, name="criterion_create"),
    path("accounts/criterion/<int:criterion_id>/edit/", views.criterion_edit, name="criterion_edit"),
    path("problem/all/", views.business_problem_all, name="business_problem_all"),
    path("problem/create/", views.business_problem_create, name="business_problem_create"),
    path("problem/<int:business_problem_id>/", views.business_problem_detail, name="business_problem_detail"),
    path("problem/<int:business_problem_id>/edit/", views.business_problem_edit, name="business_problem_edit"),
    path("problem/<int:business_problem_id>/delete/", views.business_problem_delete, name="business_problem_delete"),
    path("assumption/<int:business_problem_id>/", views.assumption_create, name="assumption_create"),
    path("assumption/<int:assumption_id>/delete/", views.assumption_delete, name="assumption_delete"),
    path("assumption/<int:assumption_id>/remove/<str:related_obj>/<int:obj_id>/", views.assumption_remove_relationship, name="assumption_remove_relationship"),
    path("strategy/create/", views.strategy_create, name="strategy_create"),
    path("strategy/<int:strategy_id>/", views.strategy_detail, name="strategy_detail"),
    path("strategy/<int:strategy_id>/edit/", views.strategy_edit, name="strategy_edit"),
    path("strategy/<int:strategy_id>/delete/", views.strategy_delete, name="strategy_delete"),
    path("strategy/<int:strategy_id>/choose/", views.strategy_choose, name="strategy_choose"),
    path("strategy/<int:strategy_id>/preview/", views.strategy_preview, name="strategy_preview"),
]