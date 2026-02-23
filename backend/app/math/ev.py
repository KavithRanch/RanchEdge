"""
Thie module provides functions to calculate expected value (EV) for sports bettings.
EV is a measure of the average return of a bet, taking into account the probability of winning and the payout odds.
A positive EV indicates a profitable bet over the long time.

Functions:
- ev_per_dollar(true_prob: float, american_odds) -> float: Calculate expected value (EV) per dollar bet given true probability and american odds.
- ev_percentage(american_odds, true_prob: float) -> float: Calculate expected value (EV) percentage given american odds and true probability.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.math.odds import american_to_decimal


def ev_per_dollar(true_prob: float, american_odds) -> float:
    """Calculate expected value (EV) per dollar bet."""

    # Validate true_prob input is between 0% and 100% (exclusive)
    if not (0.0 < true_prob < 1.0):
        raise ValueError("true_prob must be between 0 and 1 (exclusive).")
    decimal_odds = american_to_decimal(american_odds)

    # Simplified EV formula when placing a wager of $1
    return (decimal_odds * true_prob) - 1


def ev_percentage(american_odds, true_prob: float) -> float:
    """Calculate expected value (EV) percentage."""

    # Returning EV as a percentage by multiplying the EV per dollar by 100
    ev = ev_per_dollar(american_odds, true_prob)
    return ev * 100
