"""
This module contains the function to seed the leagues table with initial data.

Functions:
- seed_leagues(session: Session) -> int: Seeds the leagues table with predefined data and returns the count of new leagues added.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sports import Sport
from app.models.leagues import League
from app.constants.seed_constants import SEED_LEAGUES


def seed_leagues(session: Session) -> int:
    """Seeds the leagues table with predefined data."""

    new_league_count = 0
    # Iterate through the predefined league data and add new leagues to the database
    for league_abv, sport_name, league_name in SEED_LEAGUES:
        # Check if the league already exists
        select_league = select(League).where(League.league_name == league_name)
        league_exists = session.execute(select_league).scalar_one_or_none()

        if league_exists is None:
            # Fetch the sport for the league
            select_sport = select(Sport).where(Sport.name == sport_name)
            sport = session.execute(select_sport).scalar_one()

            # If the sport does not exist, we cannot create the league
            if sport is None:
                raise ValueError(f"Sport '{sport_name}' does not exist. Cannot create league '{league_name}'.")

            # Create and add the new league
            new_league = League(league_name=league_name, sport_id=sport.id, league_abv=league_abv)
            session.add(new_league)
            new_league_count += 1

    return new_league_count
