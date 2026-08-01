from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from builds.models import Build
from .models import Pipeline
from .forms import PipelineForm
from .services import JenkinsService


@login_required
def home(request):
    return HttpResponse("Welcome to the LLM DevOps Assistant")


@login_required
def pipeline_list(request):

    pipelines = Pipeline.objects.filter(
        owner=request.user
    )

    context = {
        "pipelines": pipelines,
    }

    return render(
        request,
        "pipeline/pipeline_list.html",
        context,
    )


@login_required
def create_pipeline(request):

    projects = request.user.projects.all()

    if not projects.exists():

        messages.warning(
            request,
            "You need to create a project before creating a pipeline.",
        )

        return redirect("project_create")

    if request.method == "POST":

        form = PipelineForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            pipeline = form.save(
                commit=False
            )

            pipeline.owner = request.user

            pipeline.save()

            return redirect("pipeline_list")

    else:

        form = PipelineForm(
            user=request.user
        )

    return render(
        request,
        "pipeline/create_pipeline.html",
        {
            "form": form,
        },
    )


@login_required
def edit_pipeline(request, pipeline_id):

    pipeline = get_object_or_404(
        Pipeline,
        id=pipeline_id,
        owner=request.user,
    )

    if request.method == "POST":

        form = PipelineForm(
            request.POST,
            instance=pipeline,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "pipeline_list"
            )

    else:

        form = PipelineForm(
            instance=pipeline,
            user=request.user,
        )

    return render(
        request,
        "pipeline/edit_pipeline.html",
        {
            "form": form,
            "pipeline": pipeline,
        },
    )


@login_required
def delete_pipeline(request, pipeline_id):

    pipeline = get_object_or_404(
        Pipeline,
        id=pipeline_id,
        owner=request.user,
    )

    if request.method == "POST":

        pipeline.delete()

        return redirect(
            "pipeline_list"
        )

    return render(
        request,
        "pipeline/delete_pipeline.html",
        {
            "pipeline": pipeline,
        },
    )


@login_required
def run_pipeline(request, pipeline_id):

    pipeline = get_object_or_404(
        Pipeline,
        id=pipeline_id,
        owner=request.user,
    )

    success = JenkinsService.trigger_build(
        pipeline.jenkins_job_name
    )

    if success:

        messages.success(
            request,
            "Build triggered successfully.",
        )

    else:

        messages.error(
            request,
            "Failed to trigger Jenkins build.",
        )

    return redirect(
        "pipeline_list"
    )


@login_required
def pipeline_detail(request, pipeline_id):

    pipeline = get_object_or_404(
        Pipeline,
        id=pipeline_id,
        owner=request.user,
    )

    builds = Build.objects.filter(
        pipeline=pipeline
    ).order_by("-created_at")

    total_builds = builds.count()

    success_count = builds.filter(
        status="SUCCESS"
    ).count()

    failed_count = builds.filter(
        status="FAILED"
    ).count()

    running_count = builds.filter(
        status="RUNNING"
    ).count()

    success_rate = 0

    if total_builds:

        success_rate = round(
            (success_count / total_builds) * 100,
            2,
        )

    avg_duration = 0

    if total_builds:

        avg_duration = round(
            sum(
                build.duration
                for build in builds
            ) / total_builds,
            2,
        )

    recent_builds = builds[:10]

    context = {

        "pipeline": pipeline,

        "recent_builds": recent_builds,

        "total_builds": total_builds,

        "success_count": success_count,

        "failed_count": failed_count,

        "running_count": running_count,

        "success_rate": success_rate,

        "avg_duration": avg_duration,

    }

    return render(
        request,
        "pipeline/pipeline_detail.html",
        context,
    )