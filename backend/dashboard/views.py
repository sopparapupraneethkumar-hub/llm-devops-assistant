from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from projects.models import Project
from builds.models import Build
from pipeline.models import Pipeline
from dashboard.services.jenkins_service import trigger_build
from django.db.models import Avg

def home(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    return render(

        request,

        "home.html"

    )

@login_required
def ai_analysis(request):

    latest_build = Build.objects.order_by(
        "-created_at"
    ).first()

    if latest_build:

        return redirect(
            "build_detail",
            pk=latest_build.id,
        )

    messages.info(
        request,
        "No builds available yet."
    )

    return redirect("dashboard")

@login_required
def dashboard(request):

    builds = Build.objects.order_by("-created_at")

    total_projects = Project.objects.filter(
        owner=request.user
    ).count()

    recent_projects = Project.objects.filter(
        owner=request.user
    ).order_by("-created_at")[:5]

    context = {
        "latest_build": builds.first(),
        "total_builds": builds.count(),
        "successful_builds": builds.filter(status="SUCCESS").count(),
        "failed_builds": builds.filter(status="FAILED").count(),
        "running_builds": builds.filter(status="RUNNING").count(),
        "recent_builds": builds[:5],
        "recent_pipelines": Pipeline.objects.filter(
            owner=request.user
        ).order_by("-created_at")[:5],

        # Projects
        "total_projects": total_projects,
        "recent_projects": recent_projects,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )

@login_required
def run_build(request):

    if request.method == "POST":

        result = trigger_build()

        if result["success"]:

            messages.success(
                request,
                f"Build Queued Successfully (HTTP {result['status_code']})"
            )

        else:

            messages.error(
                request,
                f"Jenkins Error: {result['message']}"
            )

    return redirect("dashboard")


@login_required
def build_status(request):

    builds = Build.objects.order_by("-created_at")

    latest = builds.first()

    if latest is None:

        return JsonResponse({

            "latest_build": None,

            "kpis": {

                "total_builds": 0,

                "successful_builds": 0,

                "failed_builds": 0,

                "running_builds": 0,

            }

        })

    return JsonResponse({

        "latest_build": {

            "id": latest.id,

            "build_number": latest.build_number,

            "status": latest.status,

            "duration": latest.duration,

            "summary": latest.ai_summary,

            "created_at": latest.created_at.strftime(

                "%d %b %Y %H:%M"

            ),

        },

        "kpis": {

            "total_builds": builds.count(),

            "successful_builds": builds.filter(

                status="SUCCESS"

            ).count(),

            "failed_builds": builds.filter(

                status="FAILED"

            ).count(),

            "running_builds": builds.filter(

                status="RUNNING"

            ).count(),

        }

    })

@login_required
def recent_builds(request):

    builds = Build.objects.order_by("-created_at")[:5]

    data = []

    for build in builds:

        data.append({

            "id": build.id,
            "number": build.build_number,
            "status": build.status,
            "duration": build.duration,
            "date": build.created_at.strftime("%d %b %Y %H:%M")

        })

    return JsonResponse(data, safe=False)

@login_required
def reports(request):

    builds = Build.objects.all()

    total_builds = builds.count()

    successful_builds = builds.filter(
        status="SUCCESS"
    ).count()

    failed_builds = builds.filter(
        status="FAILED"
    ).count()

    running_builds = builds.filter(
        status="RUNNING"
    ).count()

    success_rate = 0

    if total_builds:

        success_rate = round(
            (successful_builds / total_builds) * 100,
            1,
        )

    average_duration = (
        builds.aggregate(
            Avg("duration")
        )["duration__avg"]
        or 0
    )

    context = {

        "total_builds": total_builds,

        "successful_builds": successful_builds,

        "failed_builds": failed_builds,

        "running_builds": running_builds,

        "success_rate": success_rate,

        "average_duration": round(
            average_duration,
            2,
        ),

    }

    return render(

        request,

        "dashboard/reports.html",

        context,

    )