from django.db import models


class Pipeline(models.Model):
    name = models.CharField(max_length=100)

    jenkins_job_name = models.CharField(max_length=100)

    repository_url = models.URLField()

    branch = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name