from datetime import datetime
from pydantic import BaseModel


class EVOpportunityOut(BaseModel):
    """Response model for EV opportunities."""

    # Ev related fields
    ev_per_dollar: float
    edge: float
    is_positive_ev: bool

    # Odds and probability fields
    true_prob: float
    implied_prob: float
    american_odds: int
    decimal_odds: float
    true_prob_method: str

    #  Event and market details
    market_type: str
    outcome_name: str
    outcome_point: float | None

    # Metadata fields for filtering and identification
    ev_opportunity_id: int
    event_id: int
    league_id: int
    sportsbook_id: int
    market_id: int

    # Timestamp fields
    start_time: datetime
    pulled_at: datetime

    # Display fields
    league_abv: str
    sportsbook_display_name: str
    home_team_id: int
    home_team_name: str
    home_team_abv: str
    away_team_id: int
    away_team_name: str
    away_team_abv: str


class EVOppPaginationResponse(BaseModel):
    """Response model for paginated EV opportunities."""

    next_offset: int | None  # Offset for the next page of results, or None if there are no more results
    ev_opportunities: list[EVOpportunityOut]
