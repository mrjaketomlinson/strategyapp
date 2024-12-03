from django.urls import path

from project import views

urlpatterns = [
    path("", views.project_all, name="project_all"),
    path("create/", views.project_create, name="project_create"),
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("<int:project_id>/edit/", views.project_edit, name="project_edit"),
    path("<int:project_id>/delete/", views.project_delete, name="project_delete"),
    path("<int:project_id>/preview/", views.project_preview, name="project_preview"),
]