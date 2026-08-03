from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "name",
            "description",
            "repository_url",
            "default_branch",
            "technology",
            "visibility",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                }
            ),

            "repository_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username/repository.git",
                }
            ),

            "jenkins_job": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "python-demo-pipeline",
                }
            ),

            "default_branch": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "main",
                }
            ),
        }