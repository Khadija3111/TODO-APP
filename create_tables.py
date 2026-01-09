import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.database import engine
from backend.models.user import User
from backend.models.task import Task
from sqlmodel import SQLModel

# Create all tables
print("Creating tables...")
SQLModel.metadata.create_all(engine)
print("Tables created successfully!")