from django import forms
from .models import Pipeline
from projects.models import Project


class PipelineForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["project"].queryset = Project.objects.filter(
                owner=user
            )

    class Meta:
        model = Pipeline
        fields = [
            "project",
            "name",
            "repository_url",
            "branch",
            "jenkins_job_name",
            "description",
        ]

    def clean_name(self):

        name = self.cleaned_data["name"]

        if Pipeline.objects.filter(name=name).exists():
            raise forms.ValidationError(
                "Pipeline with this name already exists."
            )

        return name

    def clean_branch(self):

        branch = self.cleaned_data["branch"]

        allowed = [
            "main",
            "develop",
        ]

        if branch.startswith("feature/"):
            return branch

        if branch.startswith("bugfix/"):
            return branch

        if branch not in allowed:
            raise forms.ValidationError(
                "Branch must be main, develop, feature/* or bugfix/*."
            )

        return branch