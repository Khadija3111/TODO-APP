import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import app
from backend.api.auth import register
from backend.models.user import UserCreate
from backend.utils.database import get_session
from sqlmodel import Session, create_engine
from backend.utils.database import DATABASE_URL

# Create a test session
engine = create_engine(DATABASE_URL)
session = Session(engine)

# Test the registration function directly
try:
    user_data = UserCreate(email="test@example.com", password="testpassword")
    result = register(user_data, session)
    print("Registration successful:", result)
except Exception as e:
    print(f"Error during registration: {e}")
    import traceback
    traceback.print_exc()