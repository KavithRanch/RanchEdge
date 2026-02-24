"""
This module provides a CLI command to ingest odds data from the OddsApi into the database.
It allows users to specify the sport/league, markets, and sportsbooks to fetch odds for, and then processes the data to create a new OddsSnapshot and associated Events, Markets, and Prices in the database.

Author: Kavith Ranchagoda
Last Updated:
"""

import logging
import argparse
from app.db.session import SessionLocal
from app.data_ingest.odds.ingest import ingest_odds
from app.constants.seed_constants import (
    SPORTSBOOK_KEYS,
    DEFAULT_MARKETS,
    SPORT_LEAGUE_KEYS,
)


def parse_args() -> argparse.Namespace:
    """Set up argument parser for CLI and return parsed arguments."""

    # Set up argument parser for CLI
    argparser = argparse.ArgumentParser(description="Ingest odds from OddsApi into database")

    # Arguments to specify sport/league, markets, and sportsbooks for odds ingestion
    argparser.add_argument(
        "--sport_league",
        required=True,
        help="<sport>_<league> in simple case",
        choices=SPORT_LEAGUE_KEYS,
    )
    argparser.add_argument(
        "--markets",
        nargs="+",
        default=None,
        help="Market keys in simple case",
        choices=DEFAULT_MARKETS,
    )
    argparser.add_argument(
        "--sportsbooks",
        nargs="+",
        default=None,
        help="Sportsbook keys in simple case",
        choices=SPORTSBOOK_KEYS,
    )
    return argparser.parse_args()


def normalize_list(values: list[str] | None) -> list[str] | None:
    """Lowercase + strip; return None if empty."""
    if not values:
        return None

    # Strip whitespace and convert to lowercase, filtering out empty values
    cleaned = [v.strip().lower() for v in values if v and v.strip()]
    return cleaned or None


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    # Extract and normalize arguments
    sport_league = args.sport_league
    markets = normalize_list(args.markets) or DEFAULT_MARKETS
    sportsbooks = normalize_list(args.sportsbooks) or SPORTSBOOK_KEYS

    # Validate that provided markets and sportsbooks are valid options
    if args.markets:
        invalid = set(markets) - set(DEFAULT_MARKETS)
        if invalid:
            raise SystemExit(f"Invalid market(s): {sorted(invalid)}")

    if args.sportsbooks:
        invalid = set(sportsbooks) - set(SPORTSBOOK_KEYS)
        if invalid:
            raise SystemExit(f"Invalid sportsbook(s): {sorted(invalid)}")

    logging.info(
        "Ingest odds starting: league=%s | markets=%s | books=%s",
        sport_league,
        markets,
        sportsbooks,
    )

    # Ingest odds and create snapshot in the database, logging the resulting snapshot ID and counts of inserted records
    with SessionLocal.begin() as session:
        snapshot_id, counts = ingest_odds(
            session,
            sport_league,
            markets,
            sportsbooks,
        )

    logging.info(f"Snapshot #{snapshot_id} created")
    logging.info(f"Inserted counts: {counts}")


if __name__ == "__main__":
    main()
