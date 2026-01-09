#!/usr/bin/env python3
"""
Simple test script to verify Neon PostgreSQL database connectivity.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports to ensure modules are available."""
    try:
        print("Testing basic imports...")

        # Test SQLModel import
        from sqlmodel import SQLModel, Field
        print("[SUCCESS] SQLModel imported successfully")

        # Test database connection
        from backend.utils.database import engine
        print("[SUCCESS] Database engine created successfully")

        # Test models import
        from models.task import Task
        print("[SUCCESS] Task model imported successfully")

        # Test TaskStore import
        from services.task_store import TaskStore
        print("[SUCCESS] TaskStore imported successfully")

        print("\n[SUCCESS] All basic imports successful!")
        return True

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test actual database connection."""
    try:
        print("\nTesting database connection...")

        from backend.utils.database import engine
        from sqlmodel import text

        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("[SUCCESS] Database connection established")
            return True

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting database integration verification...\n")

    # Test basic imports first
    if not test_basic_imports():
        print("\n[FAILURE] Basic imports failed")
        sys.exit(1)

    # Test database connection
    if not test_database_connection():
        print("\n[FAILURE] Database connection failed")
        sys.exit(1)

    print("\n[SUCCESS] All database integration tests passed!")
    print("Neon PostgreSQL database is successfully integrated with the Todo application.")