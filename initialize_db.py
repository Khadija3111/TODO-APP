#!/usr/bin/env python3
"""
Script to initialize the database tables
"""

import sys
import os

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def initialize_database():
    print("Initializing database tables...")

    try:
        from backend.utils.database import create_db_and_tables
        print("Creating database tables...")
        create_db_and_tables()
        print("Database tables created successfully!")

        # Verify that the database file exists
        import os
        db_path = os.path.join(os.path.dirname(__file__), 'backend', 'todo_app.db')
        if os.path.exists(db_path):
            print(f"Database file exists: {db_path}")
            print(f"Database file size: {os.path.getsize(db_path)} bytes")
        else:
            print("Database file does not exist!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    initialize_database()