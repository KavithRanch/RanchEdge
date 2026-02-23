"""
This module sets up the SQLAlchemy engine for database interactions.
It creates an engine instance that can be used throughout the application from the DB URL.

Author: Kavith Ranchagoda
Last Updated:
"""

import os
from sqlalchemy import create_engine

# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure the DATABASE_URL is set else raise an error
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
