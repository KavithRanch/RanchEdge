import logging
from sqlalchemy import delete, select, and_, or_
from app.models.prices import Price
from app.models.markets import Market
from app.models.ev_opportunities import EvOpportunity
from app.models.true_probabilities import TrueProbability
from app.constants.enums import DEFAULT_TP_METHOD
from app.math.ev import ev_per_dollar
from app.math.odds import american_to_decimal, decimal_to_implied_probability


def generate_ev_opportunities(session, odds_snapshot_id: int, min_ev: float) -> int:
    logger = logging.getLogger(__name__)
    print(min_ev)

    # Delete existing EV opportunities for the given odds snapshot
    session.execute(
        delete(EvOpportunity).where(EvOpportunity.odds_snapshot_id == odds_snapshot_id)
    )

    # Pull all records allocated to one snapshot
    stmt = (
        select(
            Price,
            TrueProbability.id,
            TrueProbability.true_prob,
            Market.event_id,
        )
        .join(
            TrueProbability,
            and_(
                Price.market_id == TrueProbability.market_id,
                Price.outcome_name == TrueProbability.outcome_name,
                Price.odds_snapshot_id == TrueProbability.odds_snapshot_id,
                TrueProbability.method == DEFAULT_TP_METHOD,
                or_(
                    Price.outcome_point == TrueProbability.outcome_point,
                    and_(
                        TrueProbability.outcome_point.is_(None),
                        Price.outcome_point.is_(None),
                    ),
                ),
            ),
        )
        .join(Market, Market.id == Price.market_id)
        .where(Price.odds_snapshot_id == odds_snapshot_id)
    )

    prices_tp = session.execute(stmt).fetchall()

    ev_count = 0
    for price, tp_id, true_prob, event_id in prices_tp:
        tp = float(true_prob)
        ev = ev_per_dollar(tp, price.american_odds)
        if ev > min_ev:
            ev_opportunity = EvOpportunity(
                odds_snapshot_id=price.odds_snapshot_id,
                price_id=price.id,
                true_probability_id=tp_id,
                event_id=event_id,
                market_id=price.market_id,
                sportsbook_id=price.sportsbook_id,
                ev_per_dollar=ev,
                edge=tp
                - decimal_to_implied_probability(
                    american_to_decimal(price.american_odds)
                ),
                is_positive_ev=ev > 0,
            )

            session.add(ev_opportunity)
            ev_count += 1
            logger.debug(
                "+EV of %.2f%% found for market_id=%d, sportsbook_id=%d, price_id=%d",
                ev * 100,
                price.market_id,
                price.sportsbook_id,
                price.id,
            )

    return ev_count
