from django.db import models
from django.contrib.auth.models import User
from pipeline.models import Pipeline

class Build(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="builds"
    )
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name="builds"
    )

    build_number = models.IntegerField()
    project_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    duration = models.IntegerField()
    console_log = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build #{self.build_number} ({self.status})"