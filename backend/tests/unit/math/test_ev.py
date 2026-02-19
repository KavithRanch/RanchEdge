import pytest
from app.math.ev import ev_per_dollar


def test_ev_fair_even_odds_is_zero():
    assert ev_per_dollar(0.5, 100) == pytest.approx(0.0, abs=1e-9)
    assert ev_per_dollar(0.5, -100) == pytest.approx(0.0, abs=1e-9)


def test_ev_zero_odds_raises():
    with pytest.raises(ValueError):
        ev_per_dollar(0.5, 0)
