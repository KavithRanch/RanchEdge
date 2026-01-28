from datetime import datetime, timezone
from sqlalchemy import select

from app.models.leagues import League
from app.models.markets import Market
from app.models.price import Price
from app.models.sportsbooks import Sportsbook
from app.models.odds_snapshot import OddsSnapshot
from app.models.events import Event
from app.models.teams import Team

from app.data_ingest.odds.oddsapi_client import fetch_odds
from util.datetime import iso_to_datetime, format_datetime

SOURCE = "OddsAPI"


def get_id(session, stmt):
    return session.execute(stmt).scalar_one()


def ingest_odds(session, sport: str, markets: list[str], bookmakers: list[str]) -> None:
    pulled_at = datetime.now(timezone.utc)
    odds_json_response = fetch_odds(sport, markets, bookmakers)

    new_snapshot = OddsSnapshot(
        pulled_at=pulled_at,
        source=SOURCE,
    )
    session.add(new_snapshot)
    session.flush()

    # Process and store odds_json_response into the database using the session
    for event in odds_json_response:
        event_id = event["id"]
        league = event["sport_title"]
        home_team = event["home_team"]
        away_team = event["away_team"]

        league_id = get_id(
            session, select(League.id).where(League.league_name == league)
        )
        home_team_id = get_id(
            session, select(Team.id).where(Team.team_name == home_team)
        )
        away_team_id = get_id(
            session, select(Team.id).where(Team.team_name == away_team)
        )

        commence_time = iso_to_datetime(event["commence_time"])

        print(
            f"Processing event ({event_id}): {home_team} vs {away_team} at {format_datetime(commence_time)} with odds data."
        )

        event_db = session.execute(
            select(Event).where(
                Event.source == SOURCE, Event.source_event_id == event_id
            )
        ).scalar_one_or_none()

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
            session.flush()
        else:
            event_db.start_time = commence_time

        # Nested loops to handle markets and prices
        for bookmaker in event["bookmakers"]:
            sportsbook_id = get_id(
                session,
                select(Sportsbook.id).where(
                    Sportsbook.sportsbook_name == bookmaker["key"]
                ),
            )

            for market in bookmaker["markets"]:

                market_type = market["key"]
                period = "full_game"
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
                    session.flush()

                for outcome in market["outcomes"]:
                    outcome_name = outcome["name"]
                    american_odds = outcome["price"]
                    outcome_point = outcome.get("point")

                    stmt = select(Price).where(
                        Price.market_id == market_db.id,
                        Price.sportsbook_id == sportsbook_id,
                        Price.snapshot_id == new_snapshot.id,
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
                            snapshot_id=new_snapshot.id,
                            american_odds=american_odds,
                            outcome_name=outcome_name,
                            outcome_point=outcome_point,
                        )
                        session.add(price_db)
