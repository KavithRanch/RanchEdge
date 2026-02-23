"""
This module provides all odds-manipulation related functions required for sports betting calculations.

Functions:
- american_to_decimal(american_odds: float) -> float: Convert American odds (e.g. +150, -110) to Decimal odds (2.5, 1.91).
- decimal_to_implied_probability(decimal_odds: float) -> float: Convert Decimal odds to Implied Probability.
    - Implied Probability is the probability of an outcome implied by the odds given by sportsbooks.
    - These still have the sportsbook's margin built in so when looking at both sides of an event, they add up to >100%.
    - Example: decimal_to_implied_probability(2.5) returns 0.4 (or 40% implied probability).

Author: Kavith Ranchagoda
Last Updated:
"""


def american_to_decimal(american_odds: float) -> float:
    """Convert American odds (e.g. +150, -110) to Decimal odds."""
    # Handle edge case where American odds is zero
    if american_odds == 0:
        raise ValueError("American odds cannot be zero.")

    # Regular handling of American odds
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1


def decimal_to_implied_probability(decimal_odds: float) -> float:
    """Convert Decimal odds to Implied Probability."""
    return 1 / decimal_odds
