import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from sqlalchemy import select, delete

from app.db.session import SessionLocal
from app.constants.enums import DEFAULT_TP_METHOD
from app.services.ev_opportunities import generate_ev_opportunities

from app.models.leagues import League
from app.models.teams import Team
from app.models.sportsbooks import Sportsbook

from app.models.events import Event
from app.models.markets import Market
from app.models.odds_snapshots import OddsSnapshot
from app.models.prices import Price
from app.models.true_probabilities import TrueProbability
from app.models.ev_opportunities import EvOpportunity


@pytest.fixture()
def session():
    """
    Plain session fixture (not Session.begin()) so the test can commit
    setup data before running the job in separate transactions.
    """
    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


def test_generate_ev_opportunities_positive_only_and_idempotent(session):
    # --- Arrange: use existing seeded rows ---
    league = session.execute(select(League).limit(1)).scalars().first()
    assert league is not None, "No seeded leagues found."

    teams = (
        session.execute(select(Team).where(Team.league_id == league.id).limit(2))
        .scalars()
        .all()
    )
    assert len(teams) >= 2, "Need at least 2 seeded teams in the same league."
    home_team, away_team = teams[0], teams[1]
    assert home_team.id != away_team.id

    sportsbook = (
        session.execute(select(Sportsbook).where(Sportsbook.is_active).limit(1))
        .scalars()
        .first()
    )
    assert sportsbook is not None, "No seeded active sportsbooks found."

    # Create dynamic rows for this test
    event = Event(
        league_id=league.id,
        home_team_id=home_team.id,
        away_team_id=away_team.id,
        source="test",
        source_event_id=str(uuid.uuid4()),
        start_time=datetime.now(timezone.utc),
    )
    session.add(event)
    session.flush()

    market = Market(
        event_id=event.id,
        market_type="moneyline",
        period="full_game",
        line=None,
    )
    session.add(market)
    session.flush()

    snapshot = OddsSnapshot(
        pulled_at=datetime.now(timezone.utc),
        source="test",
    )
    session.add(snapshot)
    session.flush()

    # Two prices (same sportsbook) but different outcomes -> allowed by unique constraint
    # HOME should be +EV, AWAY should be -EV (so only HOME gets stored)
    price_home = Price(
        market_id=market.id,
        sportsbook_id=sportsbook.id,
        odds_snapshot_id=snapshot.id,
        american_odds=110,  # decimal 2.10
        outcome_name="HOME",
        outcome_point=None,
    )
    price_away = Price(
        market_id=market.id,
        sportsbook_id=sportsbook.id,
        odds_snapshot_id=snapshot.id,
        american_odds=-140,  # decimal ~1.714
        outcome_name="AWAY",
        outcome_point=None,
    )
    session.add_all([price_home, price_away])
    session.flush()

    tp_home = TrueProbability(
        odds_snapshot_id=snapshot.id,
        market_id=market.id,
        outcome_name="HOME",
        outcome_point=None,
        true_prob=Decimal("0.55"),  # makes +110 +EV
        method=DEFAULT_TP_METHOD,
    )
    tp_away = TrueProbability(
        odds_snapshot_id=snapshot.id,
        market_id=market.id,
        outcome_name="AWAY",
        outcome_point=None,
        true_prob=Decimal("0.45"),  # makes -140 -EV
        method=DEFAULT_TP_METHOD,
    )
    session.add_all([tp_home, tp_away])
    session.flush()

    # Commit setup so separate job runs can see the data
    session.commit()

    # --- Act: run twice in separate transactions to confirm idempotency ---
    with SessionLocal.begin() as s1:
        inserted_1 = generate_ev_opportunities(
            s1, odds_snapshot_id=snapshot.id, min_ev=0.0
        )

    with SessionLocal.begin() as s2:
        inserted_2 = generate_ev_opportunities(
            s2, odds_snapshot_id=snapshot.id, min_ev=0.0
        )

    # --- Assert + Cleanup in a fresh transaction ---
    with SessionLocal.begin() as s3:
        assert (
            inserted_1 == inserted_2
        ), "Second run should insert same number of rows (delete+rebuild)."
        assert inserted_1 == 1, "Only the HOME side should be +EV and stored."

        opps = (
            s3.execute(
                select(EvOpportunity).where(
                    EvOpportunity.odds_snapshot_id == snapshot.id
                )
            )
            .scalars()
            .all()
        )
        assert len(opps) == 1

        opp = opps[0]
        assert opp.price_id == price_home.id
        assert opp.true_probability_id == tp_home.id
        assert opp.market_id == market.id
        assert opp.event_id == event.id
        assert opp.sportsbook_id == sportsbook.id
        assert opp.is_positive_ev is True

        # Column name is ev_per_dollar in your schema
        assert float(opp.ev_per_dollar) > 0.0
        assert float(opp.edge) > 0.0  # should be positive if +EV

        # --- Cleanup: delete only what we created ---
        s3.execute(
            delete(EvOpportunity).where(EvOpportunity.odds_snapshot_id == snapshot.id)
        )
        s3.execute(
            delete(TrueProbability).where(
                TrueProbability.odds_snapshot_id == snapshot.id
            )
        )
        s3.execute(delete(Price).where(Price.odds_snapshot_id == snapshot.id))
        s3.execute(delete(Market).where(Market.id == market.id))
        s3.execute(delete(Event).where(Event.id == event.id))
        s3.execute(delete(OddsSnapshot).where(OddsSnapshot.id == snapshot.id))
