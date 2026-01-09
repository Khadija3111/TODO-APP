#!/usr/bin/env python3
"""
Script to reset the database and recreate tables with the correct schema.
"""

from backend.utils.database import engine
from sqlmodel import text

def reset_database():
    """Drop and recreate all tables with the correct schema."""
    print("Resetting database...")

    # Drop all tables
    print("Dropping existing tables...")
    with engine.connect() as conn:
        # Enable DDL transactions
        conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
        conn.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
        conn.execute(text("DROP TYPE IF EXISTS priorityenum CASCADE"))
        conn.commit()

    print("Creating new tables...")
    # Import and create the tables with the new schema
    from backend.utils.database import create_db_and_tables
    create_db_and_tables()

    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()