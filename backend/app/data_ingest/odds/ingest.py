"""
This module is responsible for ingesting odds data from the OddsAPI and persisting it in the relevant database tables.
It specifically creates a new OddsSnapshot entry and updates the Events, Markets, and Prices tables based on the data retrieved from the API.

Author: Kavith Ranchagoda
Last Updated:
"""

import logging
from datetime import datetime, timezone
from sqlalchemy import select

from app.models.leagues import League
from app.models.markets import Market
from app.models.prices import Price
from app.models.sportsbooks import Sportsbook
from app.models.odds_snapshots import OddsSnapshot
from app.models.events import Event
from app.models.teams import Team

from app.data_ingest.odds.oddsapi_client import fetch_odds
from util.datetime import iso_to_datetime, format_datetime

from app.constants.enums import MarketPeriod

SOURCE = "OddsAPI"


def get_id(session, stmt, *, entity: str, value: str):
    """Helper function to execute a select statement and return the ID of the resulting object."""

    # Execute the statement and fetch the ID of the resulting object, or raise an error if not found
    obj_id = session.execute(stmt).scalar_one_or_none()
    if obj_id is None:
        raise ValueError(f"Missing {entity} for '{value}'. Did you run seed? / is the key correct?")
    return obj_id


def ingest_odds(session, sport: str, markets: list[str], bookmakers: list[str]) -> tuple[int, dict]:
    """Ingest odds data from the OddsAPI and persist it in the database.
    Returns the ID of the created OddsSnapshot and a dictionary with counts of new events, markets  for logging purposes"""

    logger = logging.getLogger(__name__)

    pulled_at = datetime.now(timezone.utc)
    odds_json_response = fetch_odds(sport, markets, bookmakers)

    new_snapshot = OddsSnapshot(
        pulled_at=pulled_at,
        source=SOURCE,
    )
    session.add(new_snapshot)
    session.flush()

    event_count, market_count, price_count = 0, 0, 0

    # Process and store odds_json_response into the database using the session
    for event in odds_json_response:
        event_id = event["id"]
        league = event["sport_title"]
        home_team = event["home_team"]
        away_team = event["away_team"]

        league_id = get_id(
            session,
            select(League.id).where(League.league_name == league),
            entity="League",
            value=league,
        )
        home_team_id = get_id(
            session,
            select(Team.id).where(Team.team_name == home_team),
            entity="Home Team",
            value=home_team,
        )
        away_team_id = get_id(
            session,
            select(Team.id).where(Team.team_name == away_team),
            entity="Away Team",
            value=away_team,
        )

        commence_time = iso_to_datetime(event["commence_time"])

        printable_time = format_datetime(commence_time)

        logger.debug(
            "Processing event %s: (%s UTC %s/%s/%s) %s @ %s.",
            event_id,
            printable_time["time"],
            printable_time["day"],
            printable_time["month"],
            printable_time["year"],
            away_team,
            home_team,
        )

        event_db = session.execute(select(Event).where(Event.source == SOURCE, Event.source_event_id == event_id)).scalar_one_or_none()

        if event_db is None:
            event_db = Event(
                league_id=league_id,
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                source=SOURCE,
                source_event_id=event_id,
                start_time=commence_time,
            )
            session.add(event_db)
            event_count += 1
            session.flush()
        else:
            event_db.start_time = commence_time

        # Nested loops to handle markets and prices
        for bookmaker in event["bookmakers"]:
            sportsbook_id = get_id(
                session,
                select(Sportsbook.id).where(Sportsbook.sportsbook_name == bookmaker["key"]),
                entity="Sportsbook",
                value=bookmaker["key"],
            )

            for market in bookmaker["markets"]:
                market_type = market["key"]
                period = MarketPeriod.FULL_GAME.value
                if market_type == "spreads":
                    line = abs(market["outcomes"][0]["point"])
                elif market_type == "totals":
                    line = market["outcomes"][0]["point"]
                else:
                    line = None

                stmt = select(Market).where(
                    Market.event_id == event_db.id,
                    Market.market_type == market_type,
                    Market.period == period,
                )

                if line is None:
                    stmt = stmt.where(Market.line.is_(None))
                else:
                    stmt = stmt.where(Market.line == line)

                market_db = session.execute(stmt).scalar_one_or_none()

                if market_db is None:
                    market_db = Market(
                        event_id=event_db.id,
                        market_type=market_type,
                        line=line,
                        period=period,
                    )
                    session.add(market_db)
                    market_count += 1
                    session.flush()

                for outcome in market["outcomes"]:
                    outcome_name = outcome["name"]
                    american_odds = outcome["price"]
                    outcome_point = outcome.get("point")

                    stmt = select(Price).where(
                        Price.market_id == market_db.id,
                        Price.sportsbook_id == sportsbook_id,
                        Price.odds_snapshot_id == new_snapshot.id,
                        Price.outcome_name == outcome_name,
                    )

                    if outcome_point is None:
                        stmt = stmt.where(Price.outcome_point.is_(None))
                    else:
                        stmt = stmt.where(Price.outcome_point == outcome_point)

                    price_db = session.execute(stmt).scalar_one_or_none()

                    if price_db is None:
                        price_db = Price(
                            market_id=market_db.id,
                            sportsbook_id=sportsbook_id,
                            odds_snapshot_id=new_snapshot.id,
                            american_odds=american_odds,
                            outcome_name=outcome_name,
                            outcome_point=outcome_point,
                        )
                        session.add(price_db)
                        price_count += 1

    return new_snapshot.id, {
        "events": event_count,
        "markets": market_count,
        "prices": price_count,
    }
