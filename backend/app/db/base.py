"""
This module defines the base class for all database models using SQLAlchemy's declarative system.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy.orm import declarative_base

# Create a base class for declarative class definitions
Base = declarative_base()
