import requests

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "python-demo-pipeline"
BUILD_NUMBER = 14

USERNAME = "praneeth"
API_TOKEN = "11f9a4d2a1b23108d979829a3a26496f08"

url = f"{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/consoleText"

response = requests.get(
    url,
    auth=(USERNAME, API_TOKEN)
)

print("Status Code:", response.status_code)

print("\nConsole Log:\n")
print(response.text)