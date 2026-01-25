# Database Folders Structure
This document contains db folder project structure

## Database Connectivity Files
1. **engine.py**
    * The engine.py file serves as the medium for connecting to Postgres. It doesn't open connections but just create the engine which will faciliate connections

2. **session.py**
    * The session.py file serves as the medium for creating sessions with the database in order to run queries, update tables and other batabase actions

3.  **base.py**
    * base.py serves as the file defining how tables should be modelled.

## Database Schema Files
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
### Seed Files
Seeding is done so that base data that other tables reference via foreign keys are set. Additionally, should the database need to be recreated, through the use of these scripts it makes it easy for the initial setup.

1. **seed_sport.py**



