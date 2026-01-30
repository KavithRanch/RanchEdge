from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.price import Price


def compute_true_probability_per_snapshot(odds_snapshot_id: int):

    with SessionLocal.begin() as session:
        # Pull all records allocated to one snapshot
        stmt = (
            select(Price)
            .where(Price.snapshot_id == odds_snapshot_id)
            .group_by(Price.market_id)
        )
        prices = session.execute(stmt).scalars().all()

        # TESTING CODE
        print(prices)

        for p in prices:
            print(f"Team: {p.outcome_name} @ odds: {p.american_odds}")

    # Go by market and remove the vig
    # Avg out the probabilities for entries with the same market and outcome name
    # That is the true probability that we can store in a True Probability object


compute_true_probability_per_snapshot(1)
