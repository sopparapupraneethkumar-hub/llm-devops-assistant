import requests

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "python-demo-pipeline"
BUILD_NUMBER = 14

USERNAME = "praneeth"
API_TOKEN = "11d9522750c755c27001dc6f1518fa2384"

url = f"{JENKINS_URL}/job/{JOB_NAME}/{BUILD_NUMBER}/consoleText"

response = requests.get(
    url,
    auth=(USERNAME, API_TOKEN)
)

print("Status Code:", response.status_code)

print("\nConsole Log:\n")
print(response.text)