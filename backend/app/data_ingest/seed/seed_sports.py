"""
This module contains the function to seed the sports table with predefined data.

Functions:
- seed_sports(session: Session) -> int: Seeds the sports table with predefined data and returns the count of new sports added.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sports import Sport
from app.constants.seed_constants import SEED_SPORTS


def seed_sports(session: Session) -> int:
    """Seeds the sports table with predefined data."""
    new_sport_count = 0
    # Iterate through the predefined sport data and add new sports to the database
    for sport in SEED_SPORTS:
        # Check if the sport already exists
        select_sport = select(Sport).where(Sport.name == sport)
        # scalar_one_or_none() returns either None if no result is found or the single result
        sport_exists = session.execute(select_sport).scalar_one_or_none()

        if sport_exists is None:
            # Create and add the new sport
            new_sport = Sport(name=sport)
            session.add(new_sport)
            new_sport_count += 1
    return new_sport_count
