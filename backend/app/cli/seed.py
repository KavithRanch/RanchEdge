import sys
import logging
from app.data_ingest.seed.seed_sports import seed_sports
from app.data_ingest.seed.seed_teams import seed_teams
from app.data_ingest.seed.seed_sportsbooks import seed_sportsbooks
from app.data_ingest.seed.seed_leagues import seed_leagues
from app.db.session import SessionLocal


def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        raise ValueError("Usage: seed [all|sports|leagues|teams|sportsbooks]")

    target = sys.argv[1]

    logging.info(f"Beginning seeding for {target}...")
    with SessionLocal.begin() as session:
        if target in ["all", "sports"]:
            new_sports_count = seed_sports(session)
            session.flush()
            logging.info("Seeding complete for sports")
        if target in ["all", "leagues"]:
            new_leagues_count = seed_leagues(session)
            session.flush()
            logging.info("Seeding complete for leagues")
        if target in ["all", "teams"]:
            new_teams_count = seed_teams(session)
            session.flush()
            logging.info("Seeding complete for teams")
        if target in ["all", "sportsbooks"]:
            new_sportsbooks_count = seed_sportsbooks(session)
            logging.info("Seeding complete for sportsbooks")

    logging.info(
        f"Seeding complete => New sports: {new_sports_count} | New leagues: {new_leagues_count} | New teams: {new_teams_count} | New sportsbooks: {new_sportsbooks_count}"
    )


if __name__ == "__main__":
    main()
