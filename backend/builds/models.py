from django.db import models
from pipeline.models import Pipeline


class Build(models.Model):
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.PROTECT,
        related_name="builds"
    )

    build_number = models.IntegerField()

    status = models.CharField(max_length=20)

    duration = models.IntegerField()

    commit_hash = models.CharField(max_length=100)

    console_log = models.TextField()

    started_at = models.DateTimeField()

    finished_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Build #{self.build_number}"