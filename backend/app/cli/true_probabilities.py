"""
This module provides a CLI command to compute true probabilities for a given odds snapshot.
It calculates the implied probabilities from the odds in the snapshot, applies a normalization to account for the bookmaker's margin, and inserts the true probabilities into the database.

Author: Kavith Ranchagoda
Last Updated:
"""

import logging
import argparse

from app.db.session import SessionLocal
from app.services.true_probabilities import compute_true_probability_per_snapshot


def main():
    logging.basicConfig(level=logging.INFO)

    # Set up argument parser for CLI
    argparser = argparse.ArgumentParser(description="Compute true probabilties for a given odds snapshot")

    # Add argument for snapshot ID
    argparser.add_argument(
        "--snapshot",
        type=int,
        required=True,
        help="Odds snapshot ID to compute true probabilities for",
    )

    # Parse the command-line arguments
    args = argparser.parse_args()
    snapshot_id = args.snapshot

    logging.info(
        "Beginning calculating true probabilities for snapshot #%s...",
        snapshot_id,
    )

    # Compute true probabilities for the specified snapshot
    with SessionLocal.begin() as session:
        new_tprob_count = compute_true_probability_per_snapshot(session, snapshot_id)

    if new_tprob_count != 0:
        logging.info(
            "True probability calculations complete for snapshot %s => rows inserted: %d",
            snapshot_id,
            new_tprob_count,
        )
    else:
        logging.error(
            "Snapshot %s not found. No true probabilities calculated.",
            snapshot_id,
        )


if __name__ == "__main__":
    main()
