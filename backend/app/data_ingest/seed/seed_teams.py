from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.leagues import League
from app.models.teams import Team
from app.constants.seed_constants import SEED_TEAMS


def seed_teams(session: Session) -> None:
    with session.begin():
        for league_abv in SEED_TEAMS:
            league = session.execute(
                select(League).where(League.league_abv == league_abv)
            ).scalar_one_or_none()
            if league is None:
                raise ValueError(
                    f"League '{league_abv}' does not exist. Cannot seed teams."
                )

            for team_name, team_abbreviation in SEED_TEAMS[league_abv]:
                # Check if the team already exists
                select_team = select(Team).where(
                    Team.team_name == team_name, Team.league_id == league.id
                )
                team_exists = session.execute(select_team).scalar_one_or_none()

                if team_exists is None:
                    # Create and add the new team
                    new_team = Team(
                        team_name=team_name,
                        team_abv=team_abbreviation,
                        league_id=league.id,
                    )
                    session.add(new_team)
