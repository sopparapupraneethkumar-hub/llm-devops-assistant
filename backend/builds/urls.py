from django.urls import path
from .views import BuildCreateView, build_detail

urlpatterns = [

    # API Endpoint
    path(
        "",
        BuildCreateView.as_view(),
        name="build-create",
    ),

    # Web Page
    path(
        "<int:pk>/",
        build_detail,
        name="build_detail",
    ),

]