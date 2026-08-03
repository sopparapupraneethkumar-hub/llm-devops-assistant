from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "ai-analysis/",
        views.ai_analysis,
        name="ai_analysis",
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

    path(
        "reports/",
        views.reports,
        name="reports",
    ),
]