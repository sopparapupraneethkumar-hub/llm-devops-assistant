import os
import requests

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/api/builds/",
)

JENKINS_URL = os.getenv(
    "JENKINS_URL",
    "http://host.docker.internal:8080",
)

JENKINS_USERNAME = os.getenv("JENKINS_USERNAME")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")

DJANGO_API_TOKEN = os.getenv(
    "DJANGO_API_TOKEN",
    "6147012ef490c338eadb11977757e89285e3d359",
)


def fetch_console_log():

    build_number = os.getenv("BUILD_NUMBER")
    job_name = os.getenv("JOB_NAME")

    url = (
        f"{JENKINS_URL.rstrip('/')}"
        f"/job/{job_name}/{build_number}/consoleText"
    )

    print("\n========== FETCH CONSOLE LOG ==========")
    print("Username      :", JENKINS_USERNAME)
    print("Token Length  :", len(JENKINS_API_TOKEN or ""))
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
            timeout=20,
        )

        print("Console Status :", response.status_code)

        if response.status_code == 200:
            print("Console Log Length :", len(response.text))
            return response.text

        print(response.text)
        return ""

    except Exception as e:

        print("ERROR :", e)
        return ""


def create_build_payload():

    return {

        "jenkins_job_name": os.getenv("JOB_NAME", ""),

        "build_number": int(
            os.getenv("BUILD_NUMBER", "0")
        ),

        "project_name": os.getenv(
            "JOB_NAME",
            ""
        ),

        "branch": os.getenv(
            "BRANCH_NAME",
            "main"
        ),

        "status": os.getenv(
            "BUILD_STATUS",
            "UNKNOWN"
        ),

        "duration": int(
            os.getenv(
                "BUILD_DURATION",
                "0"
            )
        ),

        "console_log": fetch_console_log(),

    }


def send_build_data(payload):

    headers = {

        "Authorization": f"Token {DJANGO_API_TOKEN}",

        "Content-Type": "application/json",

    }

    print("\n========== REQUEST ==========")
    print("API URL :", API_URL)
    print("Payload Keys :", payload.keys())
    print("Console Length :", len(payload["console_log"]))
    print("=============================\n")

    try:

        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=20,
        )

        print("Response :", response.status_code)
        print(response.text)

        return response

    except Exception as e:

        print(e)

        return None


def main():

    print("\n========== ENVIRONMENT ==========")

    print("BUILD_NUMBER   :", os.getenv("BUILD_NUMBER"))
    print("JOB_NAME       :", os.getenv("JOB_NAME"))
    print("BRANCH_NAME    :", os.getenv("BRANCH_NAME"))
    print("BUILD_STATUS   :", os.getenv("BUILD_STATUS"))
    print("BUILD_DURATION :", os.getenv("BUILD_DURATION"))
    print("JENKINS_URL    :", JENKINS_URL)
    print("USERNAME       :", JENKINS_USERNAME)
    print("TOKEN LENGTH   :", len(JENKINS_API_TOKEN or ""))

    print("=================================\n")

    payload = create_build_payload()

    response = send_build_data(payload)

    if response is None:
        return

    print("\n========== DJANGO RESPONSE ==========")

    print(response.status_code)

    try:
        print(response.json())
    except Exception:
        print(response.text)

    print("=====================================")


if __name__ == "__main__":
    main()