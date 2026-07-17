from django import forms
from .models import Pipeline
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PipelineForm(forms.ModelForm):

    class Meta:
        model = Pipeline
        fields = [
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
            "develop"
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