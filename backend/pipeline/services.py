import requests
from django.conf import settings


class JenkinsService:

    @staticmethod
    def trigger_build(job_name):
        url = (
            f"{settings.JENKINS_URL}"
            f"/job/{job_name}/build"
        )

        response = requests.post(
            url,
            auth=(
                settings.JENKINS_USERNAME,
                settings.JENKINS_API_TOKEN,
            ),
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        return response.status_code in (200, 201)