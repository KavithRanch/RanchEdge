import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models.price import Price
from app.models.true_probabilities import TrueProbability
from app.services.true_probabilities import compute_true_probability_per_snapshot
from app.math.vig import remove_vig_two_way


@pytest.fixture()
def session():
    """
    Creates an in-memory SQLite database for fast integration tests.
    """
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, future=True)

    with Session.begin() as s:
        yield s


def test_compute_true_probability_per_snapshot_two_way_idempotent(session):
    snapshot_id = 1
    market_id = 10

    # Two sportsbooks
    dk = 1
    fd = 2

    # Book 1 odds: -150 / +130
    session.add_all(
        [
            Price(
                market_id=market_id,
                sportsbook_id=dk,
                snapshot_id=snapshot_id,
                american_odds=-150,
                outcome_name="TeamA",
                outcome_point=None,
            ),
            Price(
                market_id=market_id,
                sportsbook_id=dk,
                snapshot_id=snapshot_id,
                american_odds=130,
                outcome_name="TeamB",
                outcome_point=None,
            ),
        ]
    )

    # Book 2 odds: -160 / +140
    session.add_all(
        [
            Price(
                market_id=market_id,
                sportsbook_id=fd,
                snapshot_id=snapshot_id,
                american_odds=-160,
                outcome_name="TeamA",
                outcome_point=None,
            ),
            Price(
                market_id=market_id,
                sportsbook_id=fd,
                snapshot_id=snapshot_id,
                american_odds=140,
                outcome_name="TeamB",
                outcome_point=None,
            ),
        ]
    )

    session.flush()

    # Expected: remove vig per book then mean across books
    a1, b1 = remove_vig_two_way(-150, 130)
    a2, b2 = remove_vig_two_way(-160, 140)

    expected_team_a = (a1 + a2) / 2
    expected_team_b = (b1 + b2) / 2

    # --- Run computation (1st time) ---
    inserted_1 = compute_true_probability_per_snapshot(session, snapshot_id)
    assert inserted_1 == 2

    rows = (
        session.execute(
            select(TrueProbability).where(
                TrueProbability.odds_snapshot_id == snapshot_id
            )
        )
        .scalars()
        .all()
    )

    assert len(rows) == 2

    by_outcome = {r.outcome_name: float(r.true_prob) for r in rows}
    assert "TeamA" in by_outcome
    assert "TeamB" in by_outcome

    assert pytest.approx(by_outcome["TeamA"], rel=1e-6) == expected_team_a
    assert pytest.approx(by_outcome["TeamB"], rel=1e-6) == expected_team_b

    # --- Run computation again (idempotency) ---
    inserted_2 = compute_true_probability_per_snapshot(session, snapshot_id)
    assert inserted_2 == 2

    rows2 = (
        session.execute(
            select(TrueProbability).where(
                TrueProbability.odds_snapshot_id == snapshot_id
            )
        )
        .scalars()
        .all()
    )

    assert len(rows2) == 2  # no duplicates after rerun
