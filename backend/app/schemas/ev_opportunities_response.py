"""
This module defines the Pydantic model for the EV opportunities API response.
These models are used to structure the data returned by the API endpoints.

Author: Kavith Ranchagoda
Last Updated:
"""

from datetime import datetime
from pydantic import BaseModel


class EVOpportunityOut(BaseModel):
    """Response model for EV opportunities."""

    # Ev related fields (All from ev_opportunities table)
    ev_per_dollar: float
    edge: float
    is_positive_ev: bool

    # Odds and probability fields (from join on true_probabilities table)
    true_prob: float
    true_prob_method: str

    american_odds: int  # From join on prices table
    implied_prob: float  # Must be calculated from decimal odds
    decimal_odds: float  # Must be calculated from american odds

    #  Event and market details (from join on prices table except market_type)
    outcome_name: str
    outcome_point: float | None
    market_type: str  # From join on markets table

    # Metadata fields for filtering and identification
    # (All from ev_opportunities table except league_id)
    ev_opportunity_id: int
    event_id: int
    sportsbook_id: int
    market_id: int
    league_id: int  # From join on events table

    # Timestamp fields (from join on events table)
    start_time: datetime
    pulled_at: datetime  # From join on snapshot table

    # Display fields (From joins on events table, leagues, sportsbooks and teams tables)
    league_abv: str
    sportsbook_display_name: str
    home_team_id: int
    home_team_name: str
    home_team_abv: str
    away_team_id: int
    away_team_name: str
    away_team_abv: str


class EVOpportunitiesPage(BaseModel):
    """Response model for paginated EV opportunities."""

    total: int  # Total number of EV opportunities matching the filters
    next_offset: int | None  # Offset for the next page of results, or None if there are no more results
    ev_opportunities: list[EVOpportunityOut]
