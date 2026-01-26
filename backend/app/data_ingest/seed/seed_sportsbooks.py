from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sportsbooks import Sportsbook

SEED_SPORTSBOOKS: list[tuple[str, str]] = [
    ("draftkings", "DraftKings"),
    ("fanduel", "FanDuel"),
    ("betmgm", "BetMGM"),
    ("betrivers", "BetRivers"),
    ("espnbet", "ESPN Bet"),
]


def seed_sportsbooks(session: Session) -> None:
    with session.begin():
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
