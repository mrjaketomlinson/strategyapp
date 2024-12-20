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
    path("strategy/all/", views.strategy_all, name="strategy_all"),
    path("strategy/create/", views.strategy_create, name="strategy_create"),
    path("strategy/<int:strategy_id>/", views.strategy_detail, name="strategy_detail"),
    path("strategy/<int:strategy_id>/edit/", views.strategy_edit, name="strategy_edit"),
    path("strategy/<int:strategy_id>/delete/", views.strategy_delete, name="strategy_delete"),
    path("strategy/<int:strategy_id>/choose/", views.strategy_choose, name="strategy_choose"),
    path("strategy/<int:strategy_id>/preview/", views.strategy_preview, name="strategy_preview"),
    path("event/all/", views.planning_event_all, name="planning_event_all"),
    path("event/create/", views.planning_event_create, name="planning_event_create"),
    path("event/<int:planning_event_id>/", views.planning_event_detail, name="planning_event_detail"),
    path("event/<int:planning_event_id>/edit/", views.planning_event_edit, name="planning_event_edit"),
    path("event/<int:planning_event_id>/delete/", views.planning_event_delete, name="planning_event_delete"),
    path("event/<int:planning_event_id>/criterion/create/", views.criterion_weight_create, name="criterion_weight_create"),
    path("event/<int:planning_event_id>/problem/associate/", views.planning_event_business_problem_associate, name="planning_event_business_problem_associate"),
    path("event/<int:planning_event_id>/problem/<int:business_problem_id>/delete/", views.planning_event_business_problem_delete, name="planning_event_business_problem_delete"),
    path("event/<int:planning_event_id>/criterion/<int:criterion_weight_id>/edit/", views.criterion_weight_edit, name="criterion_weight_edit"),
    path("event/<int:planning_event_id>/criterion/<int:criterion_weight_id>/delete/", views.criterion_weight_delete, name="criterion_weight_delete"),
    path("event/<int:planning_event_id>/score/problem/", views.planning_event_business_problem_score, name="planning_event_business_problem_score"),
    path("event/<int:planning_event_id>/problem/set-rank/", views.planning_event_business_problem_set_rank, name="planning_event_business_problem_set_rank"),
    path("event/<int:planning_event_id>/problem/choose/", views.planning_event_business_problem_choose, name="planning_event_business_problem_choose"),
    path("event/<int:planning_event_id>/score/strategy/", views.planning_event_strategy_score, name="planning_event_strategy_score"),
    path("event/<int:planning_event_id>/strategy/set-rank/", views.planning_event_strategy_set_rank, name="planning_event_strategy_set_rank"),
    path("event/<int:planning_event_id>/strategy/choose/", views.planning_event_strategy_choose, name="planning_event_strategy_choose"),
    path("event/<int:planning_event_id>/score/project/", views.planning_event_project_score, name="planning_event_project_score"),
    path("event/<int:planning_event_id>/project/set-rank/", views.planning_event_project_set_rank, name="planning_event_project_set_rank"),
    path("event/<int:planning_event_id>/project/choose/", views.planning_event_project_choose, name="planning_event_project_choose"),
]