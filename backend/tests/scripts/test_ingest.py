from sqlalchemy.orm import Session
from app.data_ingest.odds.ingest import ingest_odds
from app.db.session import SessionLocal


def test_ingest():
    # Mock parameters
    session: Session = SessionLocal()
    sport = "basketball_nba"
    markets = ["h2h", "spreads"]
    bookmakers = ["fanduel"]

    # Call the function (this will actually make a request if not mocked)
    try:
        print("=== Running first ingestion ===")
        ingest_odds(session, sport, markets, bookmakers)
        session.commit()

        print("=== Running second ingestion ===")
        ingest_odds(session, sport, markets, bookmakers)
        session.commit()

        print("Smoke test performed succesfully.")
    except Exception as e:
        session.rollback()
        print(f"Smoke test failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    test_ingest()
