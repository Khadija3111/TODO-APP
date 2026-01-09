import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.database import create_db_and_tables
from backend.api.auth import register
from backend.models.user import UserCreate
from backend.utils.database import engine
from sqlmodel import Session

# Remove the database file if it exists
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'todo_app.db')
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Existing database file removed")
    except PermissionError:
        print("Could not remove database file - it may be in use")

# Create fresh database tables
print("Creating fresh database tables...")
create_db_and_tables()

# Test registration
print("Testing registration...")
with Session(engine) as session:
    user_data = UserCreate(email='test3@example.com', password='testpass123')
    try:
        result = register(user_data, session)
        print(f"Registration successful: {result}")
        session.commit()
        print("User saved successfully!")
    except Exception as e:
        print(f"Error during registration: {e}")
        session.rollback()