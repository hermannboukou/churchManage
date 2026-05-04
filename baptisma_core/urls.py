from django.urls import path

from . import views

app_name = "baptisma_core"

urlpatterns = [
    path("", views.candidate_dashboard, name="dashboard"),
    path("instructor/", views.instructor_dashboard, name="instructor_dashboard"),
    path("lessons/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("progress/<int:progress_id>/validate/", views.validate_progress, name="validate_progress"),
    path("api/progress-snapshot/", views.progress_snapshot, name="progress_snapshot"),
]
