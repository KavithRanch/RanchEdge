import pytest
from app.math.vig import remove_vig_two_way


def test_remove_vig_two_way_symmetric_market():
    p_a, p_b = remove_vig_two_way(-110, -110)
    assert p_a == pytest.approx(0.5, abs=1e-6)
    assert p_b == pytest.approx(0.5, abs=1e-6)
    assert (p_a + p_b) == pytest.approx(1.0, abs=1e-9)


def test_remove_vig_two_way_asymmetric_market_normalizes():
    p_a, p_b = remove_vig_two_way(-120, 100)
    assert (p_a + p_b) == pytest.approx(1.0, abs=1e-9)
    assert 0.0 < p_a < 1.0
    assert 0.0 < p_b < 1.0
    assert p_a > p_b


def test_remove_vig_two_way_zero_odds_raises():
    with pytest.raises(ValueError):
        remove_vig_two_way(0, -110)
