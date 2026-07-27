from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .forms import ProjectForm
from .models import Project
from .serializers import ProjectSerializer


@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects
        },
    )


@login_required
def project_create(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.owner = request.user

            project.save()

            return redirect("project_list")

    else:

        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form
        },
    )


@login_required
def project_update(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect("project_list")

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form
        },
    )


@login_required
def project_delete(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        project.delete()

        return redirect("project_list")

    return render(
        request,
        "projects/project_confirm_delete.html",
        {
            "project": project
        },
    )


class ProjectListCreateAPIView(ListCreateAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )