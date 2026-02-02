import logging
import argparse

from app.data_ingest.seed.seed_sports import seed_sports
from app.data_ingest.seed.seed_teams import seed_teams
from app.data_ingest.seed.seed_sportsbooks import seed_sportsbooks
from app.data_ingest.seed.seed_leagues import seed_leagues
from app.db.session import SessionLocal


def main():
    logging.basicConfig(level=logging.INFO)
    argparser = argparse.ArgumentParser(description="Setup seed tables with base data")

    argparser.add_argument(
        "--category",
        type=str,
        required=False,
        choices=["all", "sports", "leagues", "teams", "sportsbooks"],
        help="Select all or one table to seed",
        default="all",
    )

    args = argparser.parse_args()

    target = args.category

    logging.info(f"Beginning seeding for {target}...")
    with SessionLocal.begin() as session:
        if target in ("all", "sports"):
            new_sports_count = seed_sports(session)
            session.flush()
            logging.info("Seeding complete for sports")
        if target in ("all", "leagues"):
            new_leagues_count = seed_leagues(session)
            session.flush()
            logging.info("Seeding complete for leagues")
        if target in ("all", "teams"):
            new_teams_count = seed_teams(session)
            session.flush()
            logging.info("Seeding complete for teams")
        if target in ("all", "sportsbooks"):
            new_sportsbooks_count = seed_sportsbooks(session)
            logging.info("Seeding complete for sportsbooks")

    logging.info(
        "Seeding complete => New sports: %d | New leagues: %d | New teams: %d | New sportsbooks: %d",
        new_sports_count,
        new_leagues_count,
        new_teams_count,
        new_sportsbooks_count,
    )


if __name__ == "__main__":
    main()
