from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from pipeline.models import Pipeline
from ai_engine.services import (
    generate_build_summary,
    generate_ai_summary,
)

from .serializers import BuildSerializer
from .models import Build


class BuildCreateView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data.copy()

        job_name = data.pop(
            "jenkins_job_name",
            None,
        )

        serializer = BuildSerializer(
            data=data
        )

        if serializer.is_valid():

            try:

                pipeline = Pipeline.objects.get(
                    owner=request.user,
                    jenkins_job_name=job_name,
                )

            except Pipeline.DoesNotExist:

                return Response(
                    {
                        "error": "Pipeline not found."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            print("=" * 60)
            print("BUILD API RECEIVED")
            print("=" * 60)

            console_log = data.get(
                "console_log",
                "",
            )

            print(
                "Console Log Length:",
                len(console_log),
            )

            print()

            print(
                console_log[:500]
            )

            print("=" * 60)

            build = serializer.save(
                owner=request.user,
                pipeline=pipeline,
            )

            ai_summary = generate_build_summary(
                build.console_log
            )

            build.ai_summary = ai_summary

            build.save()

            generate_ai_summary(build)

            return Response(
                {
                    "message": "Build created successfully",
                    "data": BuildSerializer(build).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@login_required
def build_detail(request, pk):

    build = get_object_or_404(
        Build,
        pk=pk,
    )

    return render(
        request,
        "builds/build_detail.html",
        {
            "build": build,
        },
    )