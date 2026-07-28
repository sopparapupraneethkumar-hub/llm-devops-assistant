from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count, Q
from builds.models import Build
from projects.models import Project
from pipeline.models import Pipeline
from django.db.models.functions import TruncDate

@login_required
def dashboard(request):

    user_builds = Build.objects.filter(owner=request.user)

    latest_build = user_builds.order_by("-created_at").first()

    projects = (
        Project.objects.filter(owner=request.user)
        .prefetch_related("pipelines")
    )

    total_builds = user_builds.count()

    successful_builds = user_builds.filter(
        status="SUCCESS"
    ).count()

    failed_builds = user_builds.filter(
        status="FAILED"
    ).count()

    success_rate = 0

    if total_builds > 0:
        success_rate = round(
            (successful_builds / total_builds) * 100,
            2,
        )

    recent_builds = user_builds.order_by("-created_at")[:5]

    average_duration = (
        user_builds.aggregate(
            Avg("duration")
        )["duration__avg"] or 0
    )

    average_duration = round(average_duration, 2)
    pipeline_stats = (
        Project.objects.filter(owner=request.user)
        .prefetch_related("pipelines")
    )

    pipeline_stats = (
        Pipeline.objects.filter(owner=request.user)
        .select_related("project")
        .annotate(
            total_builds=Count("builds"),
            failed_builds=Count(
                "builds",
                filter=Q(builds__status="FAILED")
            ),
        )
        .order_by("-failed_builds", "-total_builds")
    )
    build_trends = (
        user_builds
        .annotate(
            day=TruncDate("created_at")
        )
        .values("day")
        .annotate(
            total_builds=Count("id")
        )
        .order_by("-day")
    )
    trend_labels = []
    trend_data = []

    for trend in build_trends:
        trend_labels.append(
            trend["day"].strftime("%d %b")
        )
        trend_data.append(
            trend["total_builds"]
        )
    context = {
    "latest_build": latest_build,
    "projects": projects,
    "total_builds": total_builds,
    "successful_builds": successful_builds,
    "failed_builds": failed_builds,
    "success_rate": success_rate,
    "average_duration": average_duration,
    "recent_builds": recent_builds,
    "pipeline_stats": pipeline_stats,
    "build_trends": build_trends,
    "trend_labels": trend_labels,
    "trend_data": trend_data,
    }


    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )