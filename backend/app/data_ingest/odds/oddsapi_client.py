'''
This module provides a client for fetching sports odds data from the OddsApi.
Functions:
- fetch_odds(sport: str, markets: list[str], bookmakers: list[str]): Fetches odds data for a specified sport, markets, and bookmakers from the OddsApi.

Author: Kavith Ranchagoda
Last Updated:
'''

import os
import requests

def fetch_odds(sport: str, markets: list[str], bookmakers: list[str]) -> list[dict]:
    ODDS_API_HOST = os.getenv("ODDS_API_HOST")
    ODDS_API_KEY = os.getenv("ODDS_API_KEY")

    # Ensure that the necessary environment variables are set
    if ODDS_API_HOST is None or ODDS_API_KEY is None:
        raise RuntimeError(
            "ODDS_API_HOST and ODDS_API_KEY environment variables must be set."
        )

    # Construct the request URL and parameters
    endpoint = f"/v4/sports/{sport}/odds"
    url = ODDS_API_HOST + endpoint
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": ",".join(markets),
        "bookmakers": ",".join(bookmakers),
        "oddsFormat": "american",
    }

    # Make the GET request to the OddsApi
    response = requests.get(url, params=params, timeout=10)

    try:
        # Raise an error for bad responses else download the JSON data
        response.raise_for_status()
    except requests.HTTPError as e:
        # Raise a RuntimeError with details from the response
        raise RuntimeError(
            f"OddsApi request failed ({response.status_code}): {response.text}"
        ) from e

    return response.json()

