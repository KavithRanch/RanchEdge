"""
This module provides a CLI command to seed the database with base data for sports, leagues, teams, and sportsbooks.
It allows users to specify which category of data to seed (or all) and then processes the relevant data to populate the corresponding tables in the database.
Typical use case will be to run this command once after setting up the database to ensure all necessary reference data is present for subsequent operations.

Author: Kavith Ranchagoda
Last Updated:
"""

import logging
import argparse

from app.data_ingest.seed.seed_sports import seed_sports
from app.data_ingest.seed.seed_teams import seed_teams
from app.data_ingest.seed.seed_sportsbooks import seed_sportsbooks
from app.data_ingest.seed.seed_leagues import seed_leagues
from app.db.session import SessionLocal


def main():
    logging.basicConfig(level=logging.INFO)

    # Set up argument parser for CLI
    argparser = argparse.ArgumentParser(description="Setup seed tables with base data")

    # Argument to specify which category of data to seed
    argparser.add_argument(
        "--category",
        type=str,
        required=False,
        choices=["all", "sports", "leagues", "teams", "sportsbooks"],
        help="Select all or one table to seed",
        default="all",
    )

    # Parse the arguments
    args = argparser.parse_args()
    target = args.category

    logging.info(f"Beginning seeding for {target}...")

    # Seed the database based on the specified target category
    # and log the number of new records added for each category
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
