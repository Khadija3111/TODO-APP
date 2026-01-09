import asyncio
import httpx
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_registration():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        try:
            response = await client.post("/api/auth/register",
                                       json={"email": "test@example.com", "password": "testpassword"})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except httpx.ConnectError:
            print("Could not connect to server. Make sure it's running on http://127.0.0.1:8000")
        except Exception as e:
            print(f"Error: {e}")

# Test without server first - test the actual function
import sys
import os
original_dir = os.getcwd()
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)  # Add backend to the beginning of path

from api.auth import register
from models.user import UserCreate
from utils.database import engine
from sqlmodel import Session

def test_registration_function():
    print("Testing registration function directly...")

    # Create a session
    with Session(engine) as session:
        try:
            # Create test user data with a shorter password
            user_data = UserCreate(email="test@example.com", password="testpass123")
            result = register(user_data, session)
            print(f"Registration successful: {result}")
        except Exception as e:
            print(f"Error during registration: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_registration_function()