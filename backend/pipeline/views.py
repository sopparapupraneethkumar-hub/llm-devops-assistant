from django.http import HttpResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required

from .models import Pipeline
from .forms import PipelineForm
from django.contrib import messages
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
        "pipelines": pipelines
    }

    return render(
        request,
        "pipeline/pipeline_list.html",
        context
    )

@login_required
def create_pipeline(request):

    projects = request.user.projects.all()

    if not projects.exists():
        messages.warning(
            request,
            "You need to create a project before creating a pipeline."
        )
        return redirect("project_create")

    if request.method == "POST":
        form = PipelineForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            pipeline = form.save(commit=False)

            pipeline.owner = request.user

            pipeline.save()

            return redirect("/pipelines/")

        print(form.errors)

    else:

        form = PipelineForm(
            user=request.user
        )

    return render(
        request,
        "pipeline/create_pipeline.html",
        {
            "form": form
        }
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
            return redirect("/pipelines/")

    else:

        form = PipelineForm(
            instance=pipeline,
            user=request.user,
        )

    return render(
        request,
        "pipeline/edit_pipeline.html",
        {
            "form": form
        }
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

        return redirect("/pipelines/")

    return render(
        request,
        "pipeline/delete_pipeline.html",
        {
            "pipeline": pipeline
        }
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
            "Build triggered successfully."
        )

    else:

        messages.error(
            request,
            "Failed to trigger Jenkins build."
        )

    return redirect("pipeline_list")