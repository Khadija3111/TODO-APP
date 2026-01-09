import requests
import json
import time

# Wait a moment for server to be ready
time.sleep(1)

# Test the registration endpoint
url = "http://127.0.0.1:8009/api/auth/register"
headers = {"Content-Type": "application/json"}
data = {
    "email": "minimal_test2@example.com",
    "password": "testpassword123"
}

try:
    print("Making request to:", url)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("SUCCESS: Registration endpoint is working!")
    else:
        print(f"Got status code {response.status_code}")

except requests.exceptions.ConnectionError:
    print("Could not connect to server. Make sure it's running on http://127.0.0.1:8009")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()