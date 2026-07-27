from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from builds.models import Build
from projects.models import Project


@login_required
def dashboard(request):

    user_builds = Build.objects.filter(owner=request.user)

    latest_build = user_builds.order_by("-created_at").first()

    projects = (
        Project.objects.filter(owner=request.user)
        .prefetch_related("pipelines")
    )

    total_builds = user_builds.count()
    successful_builds = user_builds.filter(status="SUCCESS").count()
    failed_builds = user_builds.filter(status="FAILED").count()

    success_rate = 0

    if total_builds > 0:
        success_rate = round(
            (successful_builds / total_builds) * 100,
            2,
        )

    recent_builds = user_builds.order_by("-created_at")[:5]

    context = {
        "latest_build": latest_build,
        "projects": projects,
        "total_builds": total_builds,
        "successful_builds": successful_builds,
        "failed_builds": failed_builds,
        "success_rate": success_rate,
        "recent_builds": recent_builds,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )