from app.data_ingest.odds.oddsapi_client import fetch_odds


def test_fetch_odds_success() -> list[dict]:
    # Mock parameters
    sport = "basketball_nba"
    markets = ["h2h", "spreads", "totals"]
    bookmakers = ["draftkings", "fanduel"]

    # Call the function (this will actually make a request if not mocked)
    try:
        odds_data = fetch_odds(sport, markets, bookmakers)
        assert isinstance(odds_data, list)  # Expecting a list of odds data
    except RuntimeError as e:
        print(f"RuntimeError occurred: {e}")

    return odds_data


if __name__ == "__main__":
    test_fetch_odds_success()
