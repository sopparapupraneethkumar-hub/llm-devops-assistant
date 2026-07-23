from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_engine.services import generate_build_summary
from .serializers import BuildSerializer


class BuildCreateView(APIView):

    def post(self, request):
        serializer = BuildSerializer(data=request.data)

        if serializer.is_valid():
            build = serializer.save()
            ai_summary = generate_build_summary(build.console_log)
            build.ai_summary = ai_summary
            build.save()

            return Response(
                {
                    "message": "Build created successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )