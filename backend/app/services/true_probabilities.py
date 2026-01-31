from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.price import Price
from app.math.vig import remove_vig_two_way
from app.math.odds import american_to_decimal, decimal_to_implied_probability


def compute_true_probability_per_snapshot(odds_snapshot_id: int):

    with SessionLocal.begin() as session:
        # Pull all records allocated to one snapshot
        stmt = select(Price).where(Price.snapshot_id == odds_snapshot_id)
        prices = session.execute(stmt).scalars().all()

        groups = {}
        for p in prices:
            key = (p.market_id, p.sportsbook_id)
            if key not in groups:
                groups[key] = []
            groups[key].append(p)

        fair_prob_by_market = {}
        for (m_id, _), price_group in groups.items():
            print(f"{price_group[0].american_odds}, {price_group[1].american_odds}")
            f_prob1, f_prob2 = remove_vig_two_way(
                price_group[0].american_odds, price_group[1].american_odds
            )

            print(f"{f_prob1}, {f_prob2}, {f_prob1 + f_prob2}")

        #     key1, key2 = (m_id, price_group[0].outcome_name), (
        #         m_id,
        #         price_group[1].outcome_name,
        #     )
        #     if key1 not in fair_prob_by_market:
        #         fair_prob_by_market[key1]
        #     if key2 not in fair_prob_by_market:
        #         fair_prob_by_market[key2]

        #     fair_prob_by_market[key1].append(f_prob1)
        #     fair_prob_by_market[key2].append(f_prob1)

        # for (m_id, outcome_name), f_prob in fair_prob_by_market.items():
        #     print(
        #         f"Market #: {m_id} | Team: {outcome_name} | # Fair Prob: {len(f_prob)}"
        #     )

    # Go by market and sportsbook to remove the vig from both outcomes
    # Go by market and outcome
    # That is the true probability that we can store in a True Probability object


compute_true_probability_per_snapshot(1)
