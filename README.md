# RanchEdge
*Backend • Data • Systems*

RanchEdge is a data-driven decision-support platform that identifies sport market pricing inefficiencies and evaluates the long-term quality of decisions under uncertainty.

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

## Versioning
- [ ] ***v1.0.0: Complete MVP***
- [ ] **v0.10.0**: Performance Dashboard
- [ ] **v0.9.0**: Bet logging (selection/outcome)
- [ ] **v0.8.0**: Basic UI dev (opportunities dashboard)
- [ ] **v0.7.0**: Basic API endpoints for EV access
- [ ] **v0.6.0**: EV Opportunities Generation
- [ ] **v0.5.0**: True probability calculation
- [x] **v0.4.0**: Odds Ingestion
    * End-to-end Odds Ingestion Pipeline implemented
        1. Pull from API
        2. Normalizes data into a relational schema 
        3. Results in time-stamped price snapshots that support historical analysis, line movement tracking, and future EV calculations. 
    * Created models for all odds ingestion related tables and seed tables
    * Created alembic migration files and applied them to the db
    * Created scripts for filling seed tables and for pulling odds from OddsApi
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
---

## Tech Stack
### Backend
- **Python**
- **FastAPI**
- **PostgreSQL (Alembis for migrations)**
- **Celery**
- **Redis**
- **SQLAlchemy**

### Frontend
- **Next.js**
- **TypeScript**

### Dev / Ops
- **Docker & docker-compose**
- **Pytest**



