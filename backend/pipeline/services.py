import requests
from django.conf import settings


class JenkinsService:

    @staticmethod
    def trigger_build(job_name):
        print("=" * 60)
        print("SETTINGS USER :", settings.JENKINS_USERNAME)
        print("TOKEN PREFIX  :", settings.JENKINS_API_TOKEN[:10])
        print("=" * 60)

        auth = (
            settings.JENKINS_USERNAME,
            settings.JENKINS_API_TOKEN,
        )

        try:

            crumb_url = (
                f"{settings.JENKINS_URL}"
                "/crumbIssuer/api/json"
            )

            crumb_response = requests.get(
                crumb_url,
                auth=auth,
                timeout=10,
            )

            headers = {}

            if crumb_response.status_code == 200:

                crumb = crumb_response.json()

                headers[
                    crumb["crumbRequestField"]
                ] = crumb["crumb"]

            build_url = (
                f"{settings.JENKINS_URL}"
                f"/job/{job_name}/build"
            )
            print("FINAL BUILD URL:")
            print(build_url)

            response = requests.post(
                build_url,
                auth=auth,
                headers=headers,
                timeout=20,
            )

            print("=" * 60)
            print("JENKINS DEBUG")
            print("=" * 60)
            print("Build URL :", build_url)
            print("Username  :", settings.JENKINS_USERNAME)
            print("Status    :", response.status_code)
            print("Headers   :", dict(response.headers))
            print("Body      :", response.text)
            print("=" * 60)

            return response.status_code in (200, 201, 202)

        except Exception as e:

            print("=" * 60)
            print("JENKINS EXCEPTION")
            print("=" * 60)
            print(e)
            print("=" * 60)

            return False