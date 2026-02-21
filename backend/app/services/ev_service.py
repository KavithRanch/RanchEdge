from operator import or_

from sqlalchemy import select
from sqlalchemy.orm import aliased

from app.constants.enums import EVSortingMethod
from app.schemas.ev_opportunities_response import EVOpportunitiesPage
from app.models import (
    EvOpportunity,
    TrueProbability,
    Price,
    Market,
    Event,
    OddsSnapshot,
    League,
    Sportsbook,
    Team,
)

HomeTeam = aliased(Team)
AwayTeam = aliased(Team)


def get_ev_opportunities(
    session,
    limit: int,
    offset: int,
    latest_snapshot: bool,
    is_positive_ev: bool,
    min_ev: float,
    league_id: int | None,
    sportsbook_id: int | None,
    sort: list[EVSortingMethod],
) -> EVOpportunitiesPage:

    # Base query selecting all necessary fields from ev_opportunities and related tables
    stmt = (
        select(
            # EV opportunity fields
            EvOpportunity.ev_per_dollar,
            EvOpportunity.edge,
            EvOpportunity.is_positive_ev,
            # True probability fields
            TrueProbability.true_prob,
            TrueProbability.method.label("true_prob_method"),
            # Price fields
            Price.american_odds,
            Price.outcome_name,
            Price.outcome_point,
            # Market type
            Market.market_type,
            # ID fields
            EvOpportunity.id.label("ev_opportunity_id"),
            EvOpportunity.event_id,
            EvOpportunity.sportsbook_id,
            EvOpportunity.market_id,
            Event.league_id,
            # Timestamp fields
            Event.start_time,
            OddsSnapshot.pulled_at,
            # Display fields
            League.league_abv,
            Sportsbook.sportsbook_display_name,
            # Join on teams table to get home and away team details
            Event.home_team_id,
            HomeTeam.team_name.label("home_team_name"),
            HomeTeam.team_abv.label("home_team_abv"),
            Event.away_team_id,
            AwayTeam.team_name.label("away_team_name"),
            AwayTeam.team_abv.label("away_team_abv"),
        )
        .select_from(EvOpportunity)
        .join(TrueProbability, EvOpportunity.true_probability_id == TrueProbability.id)
        .join(Price, EvOpportunity.price_id == Price.id)
        .join(Market, EvOpportunity.market_id == Market.id)
        .join(Event, EvOpportunity.event_id == Event.id)
        .join(OddsSnapshot, EvOpportunity.odds_snapshot_id == OddsSnapshot.id)
        .join(League, Event.league_id == League.id)
        .join(Sportsbook, EvOpportunity.sportsbook_id == Sportsbook.id)
        .join(HomeTeam, Event.home_team_id == HomeTeam.id)
        .join(AwayTeam, Event.away_team_id == AwayTeam.id)
    )

    # Apply filters based on query parameters
    if league_id is not None:
        stmt = stmt.where(Event.league_id == league_id)
    if sportsbook_id is not None:
        stmt = stmt.where(EvOpportunity.sportsbook_id == sportsbook_id)
    stmt = stmt.where(EvOpportunity.ev_per_dollar >= min_ev).where(EvOpportunity.is_positive_ev == is_positive_ev)
    # NEED LATEST SNAPSHOT PER LEAGUE


    # Apply sorting based on query parameters
    

    return EVOpportunitiesPage(
        next_offset=offset + limit if offset + limit < 100 else None,
        ev_opportunities=[],
    )
