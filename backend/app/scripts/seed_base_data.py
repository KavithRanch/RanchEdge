from app.db.session import SessionLocal

from app.data_ingest.seed.seed_sports import seed_sports
from app.data_ingest.seed.seed_leagues import seed_leagues
from app.data_ingest.seed.seed_teams import seed_teams
from app.data_ingest.seed.seed_sportsbooks import seed_sportsbooks


def main() -> None:
    """Seed the database with base data: sports, leagues, and teams."""
    session = SessionLocal()

    try:
        # Seed sports first as leagues depend on them and teams depend on leagues
        seed_sports(session)
        seed_leagues(session)
        seed_teams(session)
        seed_sportsbooks(session)
        print("Database seeding completed successfully.")
    finally:
        session.close()


# Run the main function when this script is executed
if __name__ == "__main__":
    main()
