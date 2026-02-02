import logging
import argparse

from app.db.session import SessionLocal
from app.services.true_probabilities import compute_true_probability_per_snapshot


def main():
    logging.basicConfig(level=logging.INFO)

    argparser = argparse.ArgumentParser(
        description="Compute true probabilties for a given odds snapshot"
    )
    argparser.add_argument(
        "--snapshot",
        type=int,
        required=True,
        help="Odds snapshot ID to compute true probabilities for",
    )
    args = argparser.parse_args()

    snapshot_id = args.snapshot

    logging.info(
        "Beginning calculating true probabilities for snapshot #%s...",
        snapshot_id,
    )
    with SessionLocal.begin() as session:
        new_tprob_count = compute_true_probability_per_snapshot(session, snapshot_id)

    logging.info(
        "True probability calculations complete for snapshot %s => rows inserted: %d",
        snapshot_id,
        new_tprob_count,
    )


if __name__ == "__main__":
    main()
