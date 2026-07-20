import requests
url = "http://localhost:8080/api/json"
response = requests.get(
    url,
    auth=("praneeth", "1135fbe55dea98ea28aece78d762513b6d")
)
print(response.status_code)
print(response.json())