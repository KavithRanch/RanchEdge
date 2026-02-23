"""
This module provides functions to remove the vigorish (vig) from betting odds allowing for a more accurate assessment of the true probabilities of outcomes in two-way betting markets.

Functions:
- remove_vig_two_way(odds_a: float, odds_b: float) -> Remove vig from two-way betting odds given American Odds.
    - Vig is the built-in profit margin that sportsbooks include in their odds to ensure they make a profit regardless of the outcome.
    - Removing the vig allows bettors to see the true probabilities implied by the odds.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.math.odds import american_to_decimal, decimal_to_implied_probability


def remove_vig_two_way(odds_a: float, odds_b: float) -> tuple[float, float]:
    """Remove vig from two-way betting odds given either American Odds."""

    # Convert both odds to decimal format
    dec_a = american_to_decimal(odds_a)
    dec_b = american_to_decimal(odds_b)

    # Calculate the implied probabilities for both outcomes
    prob_a = decimal_to_implied_probability(dec_a)
    prob_b = decimal_to_implied_probability(dec_b)

    # Calculate the total implied probability (which includes the vig)
    # then adjust each probability to remove the vig by taking the ratio of each probability to the total implied probability
    total_prob = prob_a + prob_b

    adj_prob_a = prob_a / total_prob
    adj_prob_b = prob_b / total_prob

    return adj_prob_a, adj_prob_b
