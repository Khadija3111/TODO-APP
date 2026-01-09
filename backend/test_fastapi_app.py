from fastapi.testclient import TestClient
from fastapi import FastAPI
from api.auth import router as auth_router

app = FastAPI(title='Todo API')
app.include_router(auth_router, prefix='/api')

client = TestClient(app)

# Test the registration endpoint using TestClient (doesn't require network)
print("Testing registration endpoint with TestClient...")

response = client.post(
    "/api/auth/register",
    json={"email": "test@example.com", "password": "testpassword123"}
)

print(f"Status Code: {response.status_code}")
if response.status_code == 200 and response.content:
    print(f"Response: {response.json()}")
    print("SUCCESS: Registration endpoint is working with TestClient!")
else:
    print(f"ERROR: Got status code {response.status_code}")
    print("Response text:", response.text)