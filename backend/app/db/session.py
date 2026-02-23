"""
This module manages database sessions using SQLAlchemy's sessionmaker.
It provides a function to get a new database session that can be used in API endpoints or other parts of the application.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy.orm import sessionmaker
from app.db.engine import engine


# Create a session factory binded to the engine from engine.py
# engine knows where the db is located and by binding it here, sessions created
# will connect to the correct database.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Function to manage database sessions
def get_db_session():
    """Get a new database session."""
    # Create a new session
    db_session = SessionLocal()

    # Ensure the session is closed after use or if errors occur
    try:
        yield db_session
    finally:
        db_session.close()
