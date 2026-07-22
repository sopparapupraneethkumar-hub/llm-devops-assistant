import os
import requests

API_URL = os.environ.get(
    "API_URL",
    "http://127.0.0.1:8000/api/builds/"
)


def create_build_payload():
    payload = {
        "build_number": int(os.environ.get("BUILD_NUMBER", 1)),
        "project_name": os.environ.get("JOB_NAME", "llm-devops-assistant"),
        "branch": os.environ.get("BRANCH_NAME", "main"),
        "status": os.environ.get("BUILD_STATUS", "SUCCESS"),
        "duration": int(os.environ.get("BUILD_DURATION", 120))
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