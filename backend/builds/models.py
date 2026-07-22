from django.db import models


class Build(models.Model):
    STATUS_CHOICES = [
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    ]

    build_number = models.IntegerField()

    project_name = models.CharField(max_length=100)

    branch = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    duration = models.IntegerField(
        help_text="Build duration in seconds"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build #{self.build_number} ({self.status})"