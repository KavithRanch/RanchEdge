import pytest
from app.math.ev import ev_per_dollar, ev_percentage, is_positive_ev


def test_ev_positive_example():
    assert ev_per_dollar(0.5, 120) == pytest.approx(0.10, abs=1e-6)
    assert ev_percentage(0.5, 120) == pytest.approx(10.0, abs=1e-6)
    assert is_positive_ev(0.5, 120) is True


def test_ev_negative_example():
    # decimal(-110) ~ 1.9091 => 0.5*1.9091 - 1 = -0.04545...
    assert ev_per_dollar(0.5, -110) == pytest.approx(-0.0454545455, abs=1e-6)
    assert is_positive_ev(0.5, -110) is False


def test_ev_fair_even_odds_is_zero():
    assert ev_per_dollar(0.5, 100) == pytest.approx(0.0, abs=1e-9)
    assert ev_per_dollar(0.5, -100) == pytest.approx(0.0, abs=1e-9)


def test_ev_zero_odds_raises():
    with pytest.raises(ValueError):
        ev_per_dollar(0.5, 0)
