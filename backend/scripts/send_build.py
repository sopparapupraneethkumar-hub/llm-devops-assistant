import os
import requests

API_URL = os.environ.get(
    "API_URL",
    "http://127.0.0.1:8000/api/builds/"
)

JENKINS_URL = "http://localhost:8080"
JENKINS_USERNAME = "praneeth"
JENKINS_API_TOKEN = "11d9522750c755c27001dc6f1518fa2384"


def fetch_console_log():
    build_number = os.environ.get("BUILD_NUMBER", 1)
    job_name = os.environ.get("JOB_NAME", "python-demo-pipeline")

    url = (
        f"{JENKINS_URL}/job/"
        f"{job_name}/"
        f"{build_number}/"
        "consoleText"
    )

    try:
        response = requests.get(
            url,
            auth=(JENKINS_USERNAME, JENKINS_API_TOKEN)
        )

        if response.status_code == 200:
            return response.text

        print(f"Failed to fetch console log ({response.status_code})")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"Error fetching console log: {e}")
        return ""


def create_build_payload():
    payload = {
        "build_number": int(os.environ.get("BUILD_NUMBER", 1)),
        "project_name": os.environ.get("JOB_NAME", "llm-devops-assistant"),
        "branch": os.environ.get("BRANCH_NAME", "main"),
        "status": os.environ.get("BUILD_STATUS", "SUCCESS"),
        "duration": int(os.environ.get("BUILD_DURATION", 120)),
        "console_log": fetch_console_log()
    }

    return payload


def send_build_data(payload):
    try:
        response = requests.post(
            API_URL,
            json=payload
        )
        return response

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def main():
    payload = create_build_payload()

    print("Payload:")
    print(payload)

    response = send_build_data(payload)

    if response is None:
        return

    print("\nStatus Code:", response.status_code)

    try:
        print("Response:")
        print(response.json())
    except ValueError:
        print("Response is not valid JSON:")
        print(response.text)


if __name__ == "__main__":
    main()