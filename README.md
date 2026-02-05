# RanchEdge
*Backend • Data • Systems*

RanchEdge is a data-driven decision-support platform that identifies sport market pricing inefficiencies and evaluates the long-term quality of decisions under uncertainty.

---

## Table of Contents
- [Motivation](#motivation)
- [Key Features](#key-features)
- [Initial Local Dev Setup](#initial-local-dev-setup)
- [Tech Stack](#tech-stack)
- [Project Roadmap](#project-roadmap)

---

## Motivation

Melting my passions for sports and data analytics, the domain used to explore these ideas is the sports betting markets, but the system design and evaluation principles generalize to other decision-making problems under uncertainty.

RanchEdge focuses on:
- Identifying opportunities where market prices are misaligned
- Making decisions based on expected value, not outcomes
- Evaluating decision quality over time rather than win/loss results

---

## Key Features

### Market-Based Opportunity Detection
- Ingests sportsbook odds for NBA player prop markets
- Converts odds to implied probabilities
- Removes bookmaker margin (vig)
- Builds a market-consensus probability
- Identifies positive expected value (+EV) opportunities

### Transparent EV Explanations
- Displays to users how expected value is calculated
- Compares prices across sportsbooks
- Surfaces assumptions and data freshness

### Decision Tracking
- Users can log bets they choose to take
- Stores the probability and EV at decision time
- Separates system output from user actions

### Performance Evaluation
- Compares **expected performance vs actual user outcomes**
- Tracks ROI and EV-based ROI over time
- Emphasizes process quality over short-term variance

### System Baseline
- Simulates a “bet everything” strategy using flat stakes
- Provides a baseline to evaluate both the system and user selection behavior

---

## Initial Local Dev Setup 

[**Click here for setup instructions**](docs/initial_setup.md)

---

## Tech Stack
<div align="center">
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/fastapi.png" alt="FastAPI"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/postgresql.png" alt="PostgreSQL"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/redis.png" alt="Redis"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/next_js.png" alt="Next.js"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/typescript.png" alt="TypeScript"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/docker.png" alt="Docker"/></code>
    <code><img width="50" src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/pytest.png" alt="Pytest"/></code>
</div>

<br><br>

<div align="center">
  <table>
    <thead>
      <tr>
        <th><b>Backend</b></th>
        <th><b>Frontend</b></th>
        <th><b>Dev / Ops</b></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td valign="top" align="center">
          Python<br>
          PostgreSQL (Alembic migrations)<br>
          Celery<br>
          Redis<br>
          SQLAlchemy
        </td>
        <td valign="top" align="center">
          Next.js<br>
          TypeScript
        </td>
        <td valign="top" align="center">
          Docker<br>
          Pytest
        </td>
      </tr>
    </tbody>
  </table>
</div>


---

## Project Roadmap
- [ ] ***v1.0.0: Complete MVP***
- [ ] **v0.10.0**: Performance Dashboard
- [ ] **v0.9.0**: Bet logging (selection/outcome)
- [ ] **v0.8.0**: Basic UI dev (opportunities dashboard)
- [ ] **v0.7.0**: Basic API endpoints for EV access
- [ ] **v0.6.0**: EV Opportunities Generation
    * New Model implemented to store calculated ev_opportunities available
- [x] **v0.5.0**: True probability calculation
    * Tidied up logging statements and relative levels
    * CLI script enables entry point through cmd for true_probability calculation
    * Created MVP true probability calculation by using vig-free mean of probabilties for each outcome
    * New Model implemented to store calculated true probabilities (one row per market per outcome)
    * Added pytest integration file which uses sqlite db
    * Created documentation for 📄[**initial local dev setup**](docs/initial_setup.md) outlining setup accurate as of the completion of v0.5.0
- [x] **v0.4.0**: Odds Ingestion
    * End-to-end Odds Ingestion Pipeline implemented
        1. Pull from API
        2. Normalizes data into a relational schema 
        3. Results in time-stamped price snapshots that support historical analysis, line movement tracking, and future EV calculations. 
    * Created models for all odds ingestion related tables and seed tables
    * Created alembic migration files and applied them to the db
    * Created scripts for filling seed tables and for pulling odds from OddsApi
    * Implemented CLI scripts to setup seeding and data persistence 
    * Designed data ingestion/persistance script
    * Documented 📄[**Odds Data Pipeline File Structure**](backend/backend_docs/db_folder_structure.md) and 📄[**DB Schema**](backend/backend_docs/db_schema.md)
- [x] **v0.3.0**: Math Engine (book edge removal + EV)
    * Implemented rudimentary odds converter and vig removal for two-way markets (Over/Under)
    * Implemented required EV calculations assuming fair probability is true prob for MVP
    * Created testing files passing 100%
    * Created documentation on the process of finding 📄[**EV**](backend/backend_docs/ev_info.md) opportunities and testing in python using 📄[**pytest**](docs/pytest_info.md)
- [x] **v0.2.0**: Database + Alembic Migration Setup
    * engine.py and session.py setup for establishing connections and sessions with database
    * simple model for sportsbook created to test functionality of Alembic migration generation and application
    * Up-to-date documentation for my personal understanding of how the different 📄[**database-related files**](backend/backend_docs/db_folder_structure.md) required work together and 📄[**general database info**](docs/database_info.md)
- [x] **v0.1.0**: Project Skeleton
    * Skeleton project structure created 
    * Basic FastAPI `/health` endpoint created for testing responsiveness
    * **backend** Dockerfile & requirements.txt setup for containerization
    * **docker-compose.yml** file setup for detailing how subsystems should be connected
    * Up-to-date documentation for my personal understanding of 📄[**docker**](docs/docker_info.md) and 📄[**fastapi**](docs/fastapi_info.md) based on usage of each tool so far
    * Documentation of 📄[**MVP**](docs/mvp.md) outlining **v1.0.0 scope**  



