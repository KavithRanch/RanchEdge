from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sportsbooks import Sportsbook
from app.constants.seed_constants import SEED_SPORTSBOOKS


def seed_sportsbooks(session: Session) -> int:
    new_sportsbook_count = 0
    for book_name, book_display_name in SEED_SPORTSBOOKS:
        # Check if the sportsbook already exists
        select_sportsbook = select(Sportsbook).where(
            Sportsbook.sportsbook_name == book_name
        )
        sportsbook_exists = session.execute(select_sportsbook).scalar_one_or_none()

        if sportsbook_exists is None:
            # Create and add the new sportsbook
            new_sportbook = Sportsbook(
                sportsbook_name=book_name, sportsbook_display_name=book_display_name
            )
            session.add(new_sportbook)
            new_sportsbook_count += 1
    return new_sportsbook_count
