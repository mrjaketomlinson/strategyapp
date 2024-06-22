from django.urls import path

from strategy import views

urlpatterns = [
    path("", views.business_problem_all, name="business_problem_all"),
    path("problem/create/", views.business_problem_create, name="business_problem_create"),
    path("problem/<int:bp_id>/", views.business_problem_detail, name="business_problem_detail")
]