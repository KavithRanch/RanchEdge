from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sports import Sport
from app.constants.seed_constants import SEED_SPORTS


def seed_sports(session: Session) -> None:
    with session.begin():
        for sport in SEED_SPORTS:
            # Check if the sport already exists
            select_sport = select(Sport).where(Sport.name == sport)
            # scalar_one_or_none() returns either None if no result is found or the single result
            sport_exists = session.execute(select_sport).scalar_one_or_none()

            if sport_exists is None:
                # Create and add the new sport
                new_sport = Sport(name=sport)
                session.add(new_sport)
