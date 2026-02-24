"""
This module contains the function to seed teams into the database.
It reads team data from the SEED_TEAMS constant and adds new teams to the database if they do not already exist. It also ensures that the associated league exists before adding teams.

Functions:
- seed_teams(session: Session) -> int: Seeds teams into the database and returns the number of new teams added.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.leagues import League
from app.models.teams import Team
from app.constants.seed_constants import SEED_TEAMS


def seed_teams(session: Session) -> int:
    """Seeds teams into the database."""
    new_teams_count = 0

    # Loop through each league abbreviation in the SEED_TEAMS constant
    for league_abv in SEED_TEAMS:
        # Check if the league exists in the database
        league = session.execute(select(League).where(League.league_abv == league_abv)).scalar_one_or_none()
        if league is None:
            raise ValueError(f"League '{league_abv}' does not exist. Cannot seed teams.")

        # Loop through each team in the league and add it to the database if it does not already exist
        for team_name, team_abbreviation in SEED_TEAMS[league_abv]:
            # Check if the team already exists
            select_team = select(Team).where(Team.team_name == team_name, Team.league_id == league.id)
            team_exists = session.execute(select_team).scalar_one_or_none()

            if team_exists is None:
                # Create and add the new team
                new_team = Team(
                    team_name=team_name,
                    team_abv=team_abbreviation,
                    league_id=league.id,
                )
                session.add(new_team)
                new_teams_count += 1
    return new_teams_count
