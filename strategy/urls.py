from django.urls import path

from strategy import views

urlpatterns = [
    path("", views.business_problem_all, name="business_problem_all"),
    path("problem/create/", views.business_problem_create, name="business_problem_create"),
    path("problem/<int:bp_id>/", views.business_problem_detail, name="business_problem_detail"),
    path("problem/<int:bp_id>/edit/", views.business_problem_edit, name="business_problem_edit"),
    path("problem/<int:bp_id>/delete/", views.business_problem_delete, name="business_problem_delete"),
    path("assumption/<str:related_obj>/<int:obj_id>/", views.assumption_create, name="assumption_create"),
    path("assumption/<int:assumption_id>/remove/<str:related_obj>/<int:obj_id>/", views.assumption_remove_relationship, name="assumption_remove_relationship"),
]