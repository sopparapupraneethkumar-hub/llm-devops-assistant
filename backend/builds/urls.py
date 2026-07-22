from django.urls import path
from .views import BuildCreateView

urlpatterns = [
    path("", BuildCreateView.as_view(), name="build-create"),
]