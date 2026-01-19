from app.math.odds import american_to_decimal


def ev_per_dollar(true_prob: float, american_odds) -> float:
    """Calculate expected value (EV) per dollar bet."""
    if not (0.0 < true_prob < 1.0):
        raise ValueError("true_prob must be between 0 and 1 (exclusive).")
    decimal_odds = american_to_decimal(american_odds)
    return (decimal_odds * true_prob) - 1


def ev_percentage(american_odds, true_prob: float) -> float:
    """Calculate expected value (EV) percentage."""
    ev = ev_per_dollar(american_odds, true_prob)
    return ev * 100


def is_positive_ev(american_odds, true_prob: float) -> bool:
    """Determine if the expected value (EV) is positive."""
    return ev_per_dollar(american_odds, true_prob) > 0
