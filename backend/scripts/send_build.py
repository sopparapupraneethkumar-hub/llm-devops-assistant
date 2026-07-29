import os
import requests

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/api/builds/"
)

JENKINS_URL = os.getenv(
    "JENKINS_URL",
    "http://localhost:8080"
)

JENKINS_USERNAME = os.getenv("JENKINS_USERNAME")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")
DJANGO_API_TOKEN = os.getenv("DJANGO_API_TOKEN")


def fetch_console_log():

    build_number = os.getenv("BUILD_NUMBER")
    job_name = os.getenv("JOB_NAME")

    url = (
        f"{JENKINS_URL}/job/"
        f"{job_name}/"
        f"{build_number}/consoleText"
    )

    print("\n========== FETCH CONSOLE LOG ==========")
    print("Job Name      :", job_name)
    print("Build Number  :", build_number)
    print("URL           :", url)
    print("=======================================\n")

    try:

        response = requests.get(
            url,
            auth=(
                JENKINS_USERNAME,
                JENKINS_API_TOKEN,
            ),
        )

        print("Console Status :", response.status_code)

        if response.status_code == 200:
            return response.text

        print(response.text)
        return ""

    except requests.exceptions.RequestException as e:

        print(e)
        return ""


def create_build_payload():

    build_number = int(os.getenv("BUILD_NUMBER", "0"))

    job_name = os.getenv("JOB_NAME", "")

    branch = os.getenv("BRANCH_NAME", "main")

    status = os.getenv("BUILD_STATUS", "UNKNOWN")

    duration = int(os.getenv("BUILD_DURATION", "0"))

    payload = {

        "jenkins_job_name": job_name,

        "build_number": build_number,

        "project_name": job_name,

        "branch": branch,

        "status": status,

        "duration": duration,

        "console_log": fetch_console_log(),

    }

    return payload


def send_build_data(payload):

    headers = {

        "Authorization": f"Token {DJANGO_API_TOKEN}",

        "Content-Type": "application/json",

    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
        )

        return response

    except requests.exceptions.RequestException as e:

        print(e)
        return None


def main():

    print("\n========== ENVIRONMENT VARIABLES ==========")
    print("BUILD_NUMBER   :", os.getenv("BUILD_NUMBER"))
    print("JOB_NAME       :", os.getenv("JOB_NAME"))
    print("BRANCH_NAME    :", os.getenv("BRANCH_NAME"))
    print("BUILD_STATUS   :", os.getenv("BUILD_STATUS"))
    print("BUILD_DURATION :", os.getenv("BUILD_DURATION"))
    print("API_URL        :", os.getenv("API_URL"))
    print("===========================================\n")

    payload = create_build_payload()

    print("\n========== PAYLOAD ==========")
    print(payload)
    print("=============================\n")

    response = send_build_data(payload)

    if response is None:
        return

    print("\n========== DJANGO RESPONSE ==========")
    print("Status Code :", response.status_code)

    try:
        print(response.json())
    except Exception:
        print(response.text)

    print("=====================================\n")


if __name__ == "__main__":
    main()