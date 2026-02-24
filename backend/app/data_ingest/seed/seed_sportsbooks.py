"""
This module contains the function to seed the sportsbooks table with predefined data.

Functions:
- seed_sportsbooks(session: Session) -> int: Seeds the sportsbooks table with predefined data and returns the count of new sportsbooks added.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sportsbooks import Sportsbook
from app.constants.seed_constants import SEED_SPORTSBOOKS


def seed_sportsbooks(session: Session) -> int:
    """Seeds the sportsbooks table with predefined data."""

    new_sportsbook_count = 0
    # Iterate through the predefined sportsbook data and add new sportsbooks to the database
    for book_name, book_display_name in SEED_SPORTSBOOKS:
        # Check if the sportsbook already exists
        select_sportsbook = select(Sportsbook).where(Sportsbook.sportsbook_name == book_name)
        sportsbook_exists = session.execute(select_sportsbook).scalar_one_or_none()

        if sportsbook_exists is None:
            # Create and add the new sportsbook
            new_sportbook = Sportsbook(sportsbook_name=book_name, sportsbook_display_name=book_display_name)
            session.add(new_sportbook)
            new_sportsbook_count += 1
    return new_sportsbook_count
