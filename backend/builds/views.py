from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ai_engine.services import generate_build_summary
from .serializers import BuildSerializer
from pipeline.models import Pipeline


class BuildCreateView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        print("\n========== REQUEST RECEIVED ==========")
        print(request.data)
        print("Authenticated User:", request.user)
        print("======================================\n")

        data = request.data.copy()

        job_name = data.pop("jenkins_job_name", None)

        print("Jenkins Job Name:", job_name)

        serializer = BuildSerializer(data=data)

        if serializer.is_valid():

            try:

                pipeline = Pipeline.objects.get(
                    owner=request.user,
                    jenkins_job_name=job_name
                )

            except Pipeline.DoesNotExist:

                print("Pipeline not found!")

                return Response(
                    {
                        "error": "Pipeline not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            build = serializer.save(
                owner=request.user,
                pipeline=pipeline
            )

            ai_summary = generate_build_summary(
                build.console_log
            )

            build.ai_summary = ai_summary
            build.save()

            print("Build Saved:", build.build_number)

            return Response(
                {
                    "message": "Build created successfully",
                    "data": BuildSerializer(build).data,
                },
                status=status.HTTP_201_CREATED,
            )

        print(serializer.errors)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )