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
    argparser = argparse.ArgumentParser(
        description="Ingest odds from OddsApi into database"
    )

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
    cleaned = [v.strip().lower() for v in values if v and v.strip()]
    return cleaned or None


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    sport_league = args.sport_league
    markets = normalize_list(args.markets) or DEFAULT_MARKETS
    sportsbooks = normalize_list(args.sportsbooks) or SPORTSBOOK_KEYS

    # Validating arguments
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
