import os
import requests

API_URL = "http://127.0.0.1:8000/api/builds/"

JENKINS_URL = "http://localhost:8080"
JENKINS_USERNAME = "praneeth"
JENKINS_API_TOKEN = "11f9a4d2a1b23108d979829a3a26496f08"


def fetch_console_log():
    build_number = "15"
    job_name = "python-demo-pipeline"

    url = f"{JENKINS_URL}/job/{job_name}/{build_number}/consoleText"

    print("\n========== DEBUG ==========")
    print("Username :", JENKINS_USERNAME)
    print("Token    :", JENKINS_API_TOKEN)
    print("Job Name :", job_name)
    print("Build No :", build_number)
    print("URL      :", url)
    print("===========================\n")

    try:
        response = requests.get(
            url,
            auth=(JENKINS_USERNAME, JENKINS_API_TOKEN)
        )

        print("Jenkins Response Status:", response.status_code)

        if response.status_code == 200:
            print("Console log fetched successfully.")
            return response.text

        print("Authentication or request failed.")
        print(response.text)
        return ""

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return ""


def create_build_payload():
    payload = {
        "build_number": 15,
        "project_name": "python-demo-pipeline",
        "branch": "main",
        "status": "SUCCESS",
        "duration": 7,
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
        print("Request failed:", e)
        return None


def main():
    payload = create_build_payload()

    print("\nPayload Sent to Django:\n")
    print(payload)

    response = send_build_data(payload)

    if response is None:
        return

    print("\nDjango Status Code:", response.status_code)

    try:
        print("\nDjango Response:")
        print(response.json())
    except ValueError:
        print(response.text)


if __name__ == "__main__":
    main()