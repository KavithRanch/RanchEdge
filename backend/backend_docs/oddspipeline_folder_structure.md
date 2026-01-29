# Data Pipeline Folders Structure
This document contains all documentation on major files used in the Odds Data Pipeline ingestion including the CLI commands

## Database Schema Files (./app/models)
1. **sports.py | leagues.py | teams.py | sportsbooks.py**
    * These schemas will rarely change are primarily seeding tables to support functionality of the rest of the dynamic tables
    * They only store meta information about their respective topics (no stats/no odds)

2. **markets.py**
    * markets.py is one of the tougher table sto understand however, it contains all lines for a specific event and specific market type. This can change as the week goes on.
    * However, it doesn't hold a line for the moneyline only for markets where there is an over/under line.
    * Many sportsbooks can point to the same market_id which helps minimize number of entries in the case where many sportsbooks are having the same line

3. **odds_snapshot.py**
    * On every pull of odds, a new entry is added here so we can keep track of how the odds change through the week

4. **events.py**
    * This table keeps up to date on upcoming events and only keep metadata related to the event itself (no odds/stats relations)
    * One per game

4. **prices.py**
    * Entries in the prices.py table contain all pertinent data regarding prices of a specific market at a certain point in time before the start of the match

## Data Ingestion Files
### Seed Files (./app/data_ingest/seed/seed_*.py)
Seeding is done so that base data that other tables reference via foreign keys are set. Additionally, should the database need to be recreated, through the use of these scripts it makes it easy for the initial setup.

### Ingestion Files (./app/data_ingest/odds)
These files are the ones used on a scheduled basis to pull, normalize and persist data into the database.

1. **oddsapi_client.py**
    * This file simply takes in parameters for the api call, performs the request and returns the JSON

2. **ingest.py**
    * The ingest.py file takes care of the normalization of the JSON response to fit the format of the db tables. 
    * It creates the odds_snapshot, event, market, price objects and persists them into the db 

## CLI Command handling (./app/cli)
These files are used to handle CLI commands to perform seeding and manually trigger the odds ingestion pipeline.

1. **seed.py**
    * Lays the foundation for all database processes by persisting sport, league, team and sportsbook data into the seed tables.
    * Arguments allow to either run individually or all in one command 
```bash
# Seed all tables 
docker compose exec backend python -m app.cli.seed all

# Can select individual table (one table/command)
docker compose exec backend python -m app.cli.seed [sports|leagues|teams|sportsbooks]
```

2. **ingest_odds.py**
    * Runs the `ingest_odds()` within `ingest.py` to run ingestion and persist data into database
    * Must have `--sport_league` tag and argument which is formatted in that way `<sport>_<league>` all in simple case.
    * `--markets` & `--sportbooks`tags are optional as they default to all supported markets and sportbooks respectfully.
    * Any parameters are validated for format and availability depending on which sports/markets/sportbooks are supported.
```bash
# Basic Ingestion of a sport + defaulting to pulling all available markets and sportsbooks
docker compose exec backend python -m app.cli.ingest_odds --sport_league basketball_nba

# Ingestion of a sport + pulling moneyline odds from fanduel and espnbet books
docker compose exec backend python -m app.cli.ingest_odds --sport_league basketball_nba --markets h2h --sportsbooks fanduel espnbet
```

## Database Connectivity Files (./app/db)
1. **engine.py**
    * The engine.py file serves as the medium for connecting to Postgres. It doesn't open connections but just create the engine which will faciliate connections

2. **session.py**
    * The session.py file serves as the medium for creating sessions with the database in order to run queries, update tables and other batabase actions

3.  **base.py**
    * base.py serves as the file defining how tables should be modelled.



