import os

import requests

from requests.auth import HTTPBasicAuth


JENKINS_URL = os.getenv(
    "JENKINS_URL",
    "http://localhost:8080",
)

JENKINS_JOB = os.getenv(
    "JENKINS_JOB",
    "python-demo-pipeline",
)

JENKINS_USER = os.getenv(
    "JENKINS_USER",
    "admin",
)

JENKINS_TOKEN = os.getenv(
    "JENKINS_API_TOKEN",
)


def trigger_build():

    crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"

    auth = HTTPBasicAuth(
        JENKINS_USER,
        JENKINS_TOKEN,
    )

    headers = {}

    try:

        crumb = requests.get(
            crumb_url,
            auth=auth,
            timeout=10,
        )

        if crumb.status_code == 200:

            data = crumb.json()

            headers[
                data["crumbRequestField"]
            ] = data["crumb"]

    except Exception:

        pass

    build_url = (
        f"{JENKINS_URL}/job/"
        f"{JENKINS_JOB}/build"
    )

    response = requests.post(
        build_url,
        auth=auth,
        headers=headers,
        timeout=20,
    )

    if response.status_code in (200, 201, 202):

        return {

            "success": True,

            "status_code": response.status_code,

            "queue_url": response.headers.get(
                "Location"
            ),

            "message": "Build queued successfully",

        }

    return {

        "success": False,

        "status_code": response.status_code,

        "queue_url": None,

        "message": response.text,

    }


def get_queue_status(queue_url):

    auth = HTTPBasicAuth(
        JENKINS_USER,
        JENKINS_TOKEN,
    )

    try:

        response = requests.get(
            f"{queue_url}api/json",
            auth=auth,
            timeout=10,
        )

        if response.status_code != 200:

            return None

        data = response.json()

        if "executable" in data:

            return {

                "status": "RUNNING",

                "build_number":
                data["executable"]["number"],

            }

        return {

            "status": "QUEUED",

        }

    except Exception:

        return None