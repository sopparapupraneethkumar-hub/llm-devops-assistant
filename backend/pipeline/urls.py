from django.urls import path
from .views import (
    pipeline_list,
    create_pipeline,
    edit_pipeline,
    delete_pipeline,
    run_pipeline,
    pipeline_detail,
)

urlpatterns = [
    path("pipelines/", pipeline_list, name="pipeline_list"),
    path("pipelines/create/", create_pipeline, name="create_pipeline"),
    path(
        "pipelines/<int:pipeline_id>/edit/",
        edit_pipeline,
        name="edit_pipeline",
    ),
    path(
        "pipelines/<int:pipeline_id>/delete/",
        delete_pipeline,
        name="delete_pipeline",
    ),
    path(
    "pipelines/<int:pipeline_id>/run/",
    run_pipeline,
    name="run_pipeline",
    ),
    path(
    "pipelines/<int:pipeline_id>/",
    pipeline_detail,
    name="pipeline_detail",
),
]