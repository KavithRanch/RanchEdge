import logging
from sqlalchemy import delete, select
from app.models.price import Price
from app.models.true_probabilities import TrueProbability
from app.math.vig import remove_vig_two_way

from app.constants.enums import TrueProbabilityMethod


def compute_true_probability_per_snapshot(session, odds_snapshot_id: int) -> int:
    logger = logging.getLogger(__name__)
    tprob_count = 0

    session.execute(
        delete(TrueProbability).where(
            TrueProbability.odds_snapshot_id == odds_snapshot_id
        )
    )

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
    for (market_id, _), price_group in groups.items():
        if len(price_group) != 2:
            logger.warning(
                "Market #%s has %d outcomes instead of 2", market_id, len(price_group)
            )
            continue

        f_prob1, f_prob2 = remove_vig_two_way(
            price_group[0].american_odds, price_group[1].american_odds
        )

        key = (market_id, price_group[0].outcome_name, price_group[0].outcome_point)
        if key not in fair_prob_by_market:
            fair_prob_by_market[key] = []
        fair_prob_by_market[key].append(f_prob1)

        key = (market_id, price_group[1].outcome_name, price_group[1].outcome_point)
        if key not in fair_prob_by_market:
            fair_prob_by_market[key] = []
        fair_prob_by_market[key].append(f_prob2)

    for (
        market_id,
        outcome_name,
        outcome_point,
    ), f_probs in fair_prob_by_market.items():
        true_prob = sum(f_probs) / len(f_probs)

        new_true_prob = TrueProbability(
            odds_snapshot_id=odds_snapshot_id,
            market_id=market_id,
            outcome_name=outcome_name,
            outcome_point=outcome_point,
            true_prob=true_prob,
            method=TrueProbabilityMethod.VIG_FREE_MEAN.value,
        )

        session.add(new_true_prob)
        tprob_count += 1
        logger.debug(
            "True probability calculated for %s at %.2f%%",
            outcome_name,
            true_prob * 100,
        )

    return tprob_count
