from sqlalchemy import and_, func, select
from sqlalchemy.orm import aliased
from app.math.odds import american_to_decimal, decimal_to_implied_probability

from app.constants.enums import EVSortingMethod
from app.schemas.ev_opportunities_response import EVOpportunitiesPage, EVOpportunityOut
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


def fetch_ev_opportunities(
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
    if latest_snapshot:
        latest_stmt = (
            select(
                Event.league_id.label("league_id"),
                func.max(OddsSnapshot.pulled_at).label("latest_pulled_at"),
            )
            .select_from(EvOpportunity)
            .join(Event, EvOpportunity.event_id == Event.id)
            .join(OddsSnapshot, EvOpportunity.odds_snapshot_id == OddsSnapshot.id)
        )

        if league_id is not None:
            latest_stmt = latest_stmt.where(Event.league_id == league_id)

        latest_snapshot_subquery = latest_stmt.group_by(Event.league_id).subquery("latest_snapshot_subquery")

        stmt = stmt.join(
            latest_snapshot_subquery,
            and_(
                Event.league_id == latest_snapshot_subquery.c.league_id,
                OddsSnapshot.pulled_at == latest_snapshot_subquery.c.latest_pulled_at,
            ),
        )

    if league_id is not None:
        stmt = stmt.where(Event.league_id == league_id)
    if sportsbook_id is not None:
        stmt = stmt.where(EvOpportunity.sportsbook_id == sportsbook_id)
    stmt = stmt.where(EvOpportunity.ev_per_dollar >= min_ev)
    stmt = stmt.where(EvOpportunity.is_positive_ev == is_positive_ev)

    # Apply sorting based on query parameters
    order_by = []
    for sort_method in sort:
        match sort_method:
            case EVSortingMethod.EV_DESC:
                order_by.append(EvOpportunity.ev_per_dollar.desc())
            case EVSortingMethod.EV_ASC:
                order_by.append(EvOpportunity.ev_per_dollar.asc())
            case EVSortingMethod.EDGE_DESC:
                order_by.append(EvOpportunity.edge.desc())
            case EVSortingMethod.EDGE_ASC:
                order_by.append(EvOpportunity.edge.asc())
            case EVSortingMethod.START_TIME_ASC:
                order_by.append(Event.start_time.asc())
            case EVSortingMethod.START_TIME_DESC:
                order_by.append(Event.start_time.desc())
            case EVSortingMethod.PULLED_AT_ASC:
                order_by.append(OddsSnapshot.pulled_at.asc())
            case EVSortingMethod.PULLED_AT_DESC:
                order_by.append(OddsSnapshot.pulled_at.desc())
    if order_by:
        stmt = stmt.order_by(*order_by)

    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = session.execute(count_stmt).scalar_one()

    stmt = stmt.limit(limit).offset(offset)
    ev_rows = session.execute(stmt).mappings().all()
    items: list[EVOpportunityOut] = []
    for row in ev_rows:
        dec = american_to_decimal(row["american_odds"])
        implied = decimal_to_implied_probability(dec)

        items.append(
            EVOpportunityOut(
                **row,
                decimal_odds=dec,
                implied_prob=implied,
            )
        )

    return EVOpportunitiesPage(
        total=total,
        next_offset=offset + limit if offset + limit < total else None,
        ev_opportunities=items,
    )
