import logging
import argparse

from app.db.session import SessionLocal
from app.services.ev_opportunities import generate_ev_opportunities


def main():
    logging.basicConfig(level=logging.INFO)

    argparser = argparse.ArgumentParser(
        description="Compute EV opportunities for a given odds snapshot"
    )
    argparser.add_argument(
        "--snapshot",
        type=int,
        required=True,
        help="Odds snapshot ID to compute EV opportunities for",
    )
    argparser.add_argument(
        "--min_ev",
        type=float,
        default=0.0,
        help="Non-neg Minimum EV threshold to consider an opportunity (defaults to 0.0)",
    )
    args = argparser.parse_args()

    snapshot_id, min_ev = args.snapshot, args.min_ev

    logging.info(
        "Beginning calculating EV opportunities for snapshot #%s (min EV: %s)...",
        snapshot_id,
        min_ev,
    )
    with SessionLocal.begin() as session:
        new_ev_count, price_count = generate_ev_opportunities(
            session, snapshot_id, min_ev
        )

    if new_ev_count != 0:
        logging.info(
            "EV opportunities calculations complete for snapshot %s => rows inserted: %d, prices analyzed: %d",
            snapshot_id,
            new_ev_count,
            price_count,
        )
    else:
        logging.error(
            "No EV opportunities inserted for snapshot %s.",
            snapshot_id,
        )


if __name__ == "__main__":
    main()
