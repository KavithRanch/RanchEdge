from app.math.odds import american_to_decimal, decimal_to_implied_probability


def remove_vig_two_way(odds_a: float, odds_b: float) -> tuple[float, float]:
    """Remove vig from two-way betting odds given either American Odds."""
    dec_a = american_to_decimal(odds_a)
    dec_b = american_to_decimal(odds_b)

    prob_a = decimal_to_implied_probability(dec_a)
    prob_b = decimal_to_implied_probability(dec_b)

    total_prob = prob_a + prob_b

    adj_prob_a = prob_a / total_prob
    adj_prob_b = prob_b / total_prob

    return adj_prob_a, adj_prob_b
