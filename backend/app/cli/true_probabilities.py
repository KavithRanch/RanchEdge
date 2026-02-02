import sys
import logging

from app.db.session import SessionLocal
from app.services.true_probabilities import compute_true_probability_per_snapshot


def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 2:
        raise ValueError("Usage: true_probs <snapshot_id>")

    try:
        snapshot_id = int(sys.argv[1])
    except ValueError:
        print("snapshot_id must be an integer")
        sys.exit(2)

    new_tprob_count = 0

    logging.info(
        f"Beginning calculating true probabilities for snapshot #{snapshot_id}..."
    )
    with SessionLocal.begin() as session:
        new_tprob_count = compute_true_probability_per_snapshot(session, snapshot_id)

    logging.info(
        f"True probability calculations complete => rows inserted: {new_tprob_count}"
    )


if __name__ == "__main__":
    main()
