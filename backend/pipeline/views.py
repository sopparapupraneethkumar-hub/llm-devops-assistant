from django.http import HttpResponse
from .models import Pipeline
from django.shortcuts import render,redirect
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from .forms import PipelineForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return HttpResponse("Welcome to the LLM DevOps Assistant")


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
    
    if request.method == "POST":

        form = PipelineForm(request.POST)
        if form.is_valid():

            pipeline = form.save(commit=False)

            pipeline.owner = request.user

            pipeline.save()

            return redirect("/pipelines/")

        print(form.errors)

    else:

        form = PipelineForm()
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
    owner=request.user
)
    if request.method == "POST":

        pipeline.name = request.POST["name"]
        pipeline.repository_url = request.POST["repository_url"]
        pipeline.branch = request.POST["branch"]
        pipeline.jenkins_job_name = request.POST["jenkins_job_name"]
        pipeline.description = request.POST["description"]

        pipeline.save()

        return redirect("/pipelines/")

    return render(
        request,
        "pipeline/edit_pipeline.html",
        {
            "pipeline": pipeline
        }
    )

@login_required
def delete_pipeline(request, pipeline_id):

    pipeline = get_object_or_404(
    Pipeline,
    id=pipeline_id,
    owner=request.user
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
