from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
    "run-build/",
    views.run_build,
    name="run_build",
    ),
    path(
    "build-status/",
    views.build_status,
    name="build_status",
    ),
    path(
    "recent-builds/",
    views.recent_builds,
    name="recent_builds",
    ),
]