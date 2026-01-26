from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sports import Sport
from app.models.leagues import League

SEED_LEAGUES: list[tuple[str, str, str]] = [
    ("nba", "basketball", "NBA"),
    ("nfl", "football", "NFL"),
]


def seed_leagues(session: Session) -> None:
    with session.begin():
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
                    raise ValueError(
                        f"Sport '{sport_name}' does not exist. Cannot create league '{league_name}'."
                    )

                # Create and add the new league
                new_league = League(
                    league_name=league_name, sport_id=sport.id, league_abv=league_abv
                )
                session.add(new_league)
