import pytest
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models.sports import Sport
from app.models.leagues import League
from app.models.teams import Team
from app.models.events import Event
from app.models.markets import Market
from app.models.odds_snapshots import OddsSnapshot
from app.models.prices import Price
from app.models.true_probabilities import TrueProbability
from app.models.ev_opportunities import EvOpportunity

from app.constants.enums import DEFAULT_TP_METHOD
from app.services.ev_opportunities import generate_ev_opportunities


@pytest.fixture()
def session():
    """Creates an in-memory SQLite database for fast integration tests."""
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, future=True)

    with Session.begin() as s:
        yield s


def test_generate_ev_opportunities_positive_only_and_idempotent(session):
    snapshot_id = 1

    # --- Minimal relational chain setup ---
    sport = Sport(name="TestSport")
    session.add(sport)
    session.flush()

    league = League(
        league_name="TestLeague",
        league_abv="TL",
        sport_id=sport.id,
    )
    session.add(league)
    session.flush()

    team_a = Team(team_name="TeamA", team_abv="TA", league_id=league.id)
    team_b = Team(team_name="TeamB", team_abv="TB", league_id=league.id)
    session.add_all([team_a, team_b])
    session.flush()

    event = Event(
        league_id=league.id,
        home_team_id=team_a.id,
        away_team_id=team_b.id,
        source="test",
        source_event_id="evt1",
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
        id=snapshot_id,
        pulled_at=datetime.now(timezone.utc),
        source="test",
    )
    session.add(snapshot)
    session.flush()

    # Prices
    price_home = Price(
        market_id=market.id,
        sportsbook_id=1,
        odds_snapshot_id=snapshot_id,
        american_odds=110,
        outcome_name="HOME",
        outcome_point=None,
    )
    price_away = Price(
        market_id=market.id,
        sportsbook_id=1,
        odds_snapshot_id=snapshot_id,
        american_odds=-140,
        outcome_name="AWAY",
        outcome_point=None,
    )
    session.add_all([price_home, price_away])
    session.flush()

    # True probabilities
    tp_home = TrueProbability(
        odds_snapshot_id=snapshot_id,
        market_id=market.id,
        outcome_name="HOME",
        outcome_point=None,
        true_prob=Decimal("0.55"),  # +EV at +110
        method=DEFAULT_TP_METHOD,
    )
    tp_away = TrueProbability(
        odds_snapshot_id=snapshot_id,
        market_id=market.id,
        outcome_name="AWAY",
        outcome_point=None,
        true_prob=Decimal("0.45"),  # -EV at -140
        method=DEFAULT_TP_METHOD,
    )
    session.add_all([tp_home, tp_away])
    session.flush()

    # --- Run EV generation (1st time) ---
    ev_count_1, price_count_1 = generate_ev_opportunities(
        session, snapshot_id, min_ev=0.0
    )
    assert price_count_1 == 2
    assert ev_count_1 == 1

    rows = (
        session.execute(
            select(EvOpportunity).where(EvOpportunity.odds_snapshot_id == snapshot_id)
        )
        .scalars()
        .all()
    )
    assert len(rows) == 1
    opp = rows[0]

    assert opp.price_id == price_home.id
    assert float(opp.ev_per_dollar) > 0.0
    assert float(opp.edge) > 0.0
    assert opp.is_positive_ev is True

    # --- Run EV generation again (idempotency) ---
    ev_count_2, price_count_2 = generate_ev_opportunities(
        session, snapshot_id, min_ev=0.0
    )
    assert price_count_2 == 2
    assert ev_count_2 == 1

    rows2 = (
        session.execute(
            select(EvOpportunity).where(EvOpportunity.odds_snapshot_id == snapshot_id)
        )
        .scalars()
        .all()
    )
    assert len(rows2) == 1  # no duplicates after rerun
