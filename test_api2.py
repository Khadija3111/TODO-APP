import requests
import json

# Test the registration endpoint
url = "http://127.0.0.1:8004/api/auth/register"
headers = {"Content-Type": "application/json"}
data = {
    "email": "testuser3@example.com",
    "password": "testpassword123"
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.ConnectionError:
    print("Could not connect to server. Make sure it's running on http://127.0.0.1:8004")
except Exception as e:
    print(f"Error: {e}")