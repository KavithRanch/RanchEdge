import pytest
from app.math.odds import american_to_decimal


def test_american_to_decimal_positive_examples():
    assert american_to_decimal(100) == 2.0
    assert american_to_decimal(150) == 2.5
    assert american_to_decimal(200) == 3.0


def test_american_to_decimal_negative_examples():
    assert american_to_decimal(-100) == 2.0
    assert american_to_decimal(-200) == 1.5
    assert american_to_decimal(-400) == 1.25
    assert american_to_decimal(-110) == pytest.approx(1.9090909091)


def test_american_to_decimal_zero_raises():
    with pytest.raises(ValueError):
        american_to_decimal(0)
