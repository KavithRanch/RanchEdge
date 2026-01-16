def american_to_decimal(american_odds: int) -> float:
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
