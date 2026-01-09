import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.api.auth import register
from backend.models.user import UserCreate
from backend.utils.database import engine
from sqlmodel import Session

# Test the registration function that's called by the endpoint
print("Testing the registration function directly...")

user_data = UserCreate(email="endpoint_test@example.com", password="testpassword123")

with Session(engine) as session:
    try:
        result = register(user_data, session)
        print(f"SUCCESS: Registration worked! User created: {result.email}, ID: {result.id}")
    except Exception as e:
        print(f"ERROR in registration function: {e}")
        import traceback
        traceback.print_exc()

print("\nTesting complete.")