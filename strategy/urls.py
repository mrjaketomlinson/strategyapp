from django.urls import path

from strategy import views

urlpatterns = [
    path("", views.business_problem_all, name="business_problem_all"),
]