import requests

url = "http://127.0.0.1:8000/api/builds/"

headers = {
    "Authorization": "Token 6147012ef490c338eadb11977757e89285e3d359",
    "Content-Type": "application/json",
}

payload = {
    "jenkins_job_name": "python-demo-pipeline",
    "build_number": 999,
    "project_name": "python-demo-pipeline",
    "branch": "main",
    "status": "SUCCESS",
    "duration": 5,
    "console_log": "Test build",
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)
print(response.text)