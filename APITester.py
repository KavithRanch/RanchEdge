from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
odds_api_key = os.getenv('ODDS_API_KEY')

# API endpoint configuration
sports_list = ["americanfootball_nfl", "basketball_nba", "icehockey_nhl", "americanfootball_ncaaf", "baseball_mlb"]
bookmakers_list = ["fanduel", "draftkings", "betrivers", "betmgm"]
markets_list = ["h2h", "spreads", "totals", "team_totals", "alternate_team_totals"]
football_markets_list = ["player_pass_tds", "player_pass_yds", "player_rush_yds", "player_reception_yds"]
basketball_markets_list = ["player_points", "player_rebounds", "player_assists", "player_threes", "player_blocks", "player_steals", "player_points_rebounds_assists", "player_points_rebounds", "player_points_assists", "player_rebounds_assists"]

# API url configuration
sports = sports_list[0]
bookmakers = bookmakers_list[0]
markets = markets_list[0]
url = "https://api.the-odds-api.com/v4/sports/" + sports + "/odds/?apiKey=" + odds_api_key + "&bookmakers=" + bookmakers + "&markets=" + markets + "&oddsFormat=decimal"

def oddsConverter(odd):
    if odd.is_integer():
        if (odd > 0):
            return "{:.2f}".format(round((odd / 100) + 1, 2))
        else:
            return "{:.2f}".format(round((100 / (odd * -1)) + 1, 2))
    else:
        if (odd > 2.00):
            return round((odd - 1) * 100)
        else:
            return round(-100 / (odd - 1))



