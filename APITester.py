from dotenv import load_dotenv
import requests
import json
import os
from _datetime import datetime

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

response = [{"id":"b516611a4ade7c4d55fcde561ed71328","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-04T00:15:00Z","home_team":"Atlanta Falcons","away_team":"Tampa Bay Buccaneers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Atlanta Falcons","price":1.75},{"name":"Tampa Bay Buccaneers","price":2.14}]}]}]},{"id":"b782886bcc4874123d3bb50e5d1e88c3","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T13:30:00Z","home_team":"Minnesota Vikings","away_team":"New York Jets","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Minnesota Vikings","price":1.65},{"name":"New York Jets","price":2.3}]}]}]},{"id":"73da5785865b6ab0852df1aa0c47994e","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"Cincinnati Bengals","away_team":"Baltimore Ravens","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Baltimore Ravens","price":1.68},{"name":"Cincinnati Bengals","price":2.24}]}]}]},{"id":"2eb8e0798cb1b1f9d0f0d414253b4e37","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"Houston Texans","away_team":"Buffalo Bills","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Buffalo Bills","price":1.89},{"name":"Houston Texans","price":1.96}]}]}]},{"id":"b727380f1b93218185ba53da28e0f6a7","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"Chicago Bears","away_team":"Carolina Panthers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Carolina Panthers","price":2.72},{"name":"Chicago Bears","price":1.49}]}]}]},{"id":"43f21c8e455914cc71d00ca0001ae85b","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"Washington Commanders","away_team":"Cleveland Browns","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Cleveland Browns","price":2.42},{"name":"Washington Commanders","price":1.6}]}]}]},{"id":"dba45197b1cd2dbafe7f83ebffd2be90","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"Jacksonville Jaguars","away_team":"Indianapolis Colts","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Indianapolis Colts","price":2.28},{"name":"Jacksonville Jaguars","price":1.66}]}]}]},{"id":"5cb3b58ed90ecfac2acac9115e08c017","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T17:00:00Z","home_team":"New England Patriots","away_team":"Miami Dolphins","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Miami Dolphins","price":1.96},{"name":"New England Patriots","price":1.89}]}]}]},{"id":"a0877d6a0f0a97e5790884008b9974c9","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T20:05:00Z","home_team":"San Francisco 49ers","away_team":"Arizona Cardinals","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Arizona Cardinals","price":3.95},{"name":"San Francisco 49ers","price":1.27}]}]}]},{"id":"9a9219cd7180fe6481e6bd9e460a7622","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T20:05:00Z","home_team":"Denver Broncos","away_team":"Las Vegas Raiders","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Denver Broncos","price":1.77},{"name":"Las Vegas Raiders","price":2.1}]}]}]},{"id":"f555a965152f8896b1cf418205724508","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T20:25:00Z","home_team":"Los Angeles Rams","away_team":"Green Bay Packers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Green Bay Packers","price":1.58},{"name":"Los Angeles Rams","price":2.44}]}]}]},{"id":"777e65cf50b4517465cea9ac9d686227","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-06T20:25:00Z","home_team":"Seattle Seahawks","away_team":"New York Giants","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"New York Giants","price":3.15},{"name":"Seattle Seahawks","price":1.38}]}]}]},{"id":"504a7b09264059083346ab086141da30","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-07T00:20:00Z","home_team":"Pittsburgh Steelers","away_team":"Dallas Cowboys","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Dallas Cowboys","price":2.16},{"name":"Pittsburgh Steelers","price":1.74}]}]}]},{"id":"5e0d59f75b7f9056461e2970aca2a6cb","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-08T00:15:00Z","home_team":"Kansas City Chiefs","away_team":"New Orleans Saints","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Kansas City Chiefs","price":1.4},{"name":"New Orleans Saints","price":3.05}]}]}]},{"id":"0dac14546d6008893a8b3b6c417472a6","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-11T00:16:00Z","home_team":"Seattle Seahawks","away_team":"San Francisco 49ers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"San Francisco 49ers","price":1.61},{"name":"Seattle Seahawks","price":2.38}]}]}]},{"id":"c1bcc8bbec33008ae587584b1b3de2d0","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T13:31:00Z","home_team":"Chicago Bears","away_team":"Jacksonville Jaguars","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Chicago Bears","price":1.86},{"name":"Jacksonville Jaguars","price":1.98}]}]}]},{"id":"fb08594af963cff8fae2f93b2e0f4269","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"Green Bay Packers","away_team":"Arizona Cardinals","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Arizona Cardinals","price":3.1},{"name":"Green Bay Packers","price":1.39}]}]}]},{"id":"c3b700ee54cf3cb44de965e6cfcb19f9","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"Baltimore Ravens","away_team":"Washington Commanders","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Baltimore Ravens","price":1.27},{"name":"Washington Commanders","price":3.95}]}]}]},{"id":"8bd202ca7bacf3396a1b774f12de0fab","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"Philadelphia Eagles","away_team":"Cleveland Browns","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Cleveland Browns","price":3.7},{"name":"Philadelphia Eagles","price":1.3}]}]}]},{"id":"febb2d674e85a32c8636ff900fffb5d2","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"New England Patriots","away_team":"Houston Texans","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Houston Texans","price":1.29},{"name":"New England Patriots","price":3.75}]}]}]},{"id":"bdc58f80a5a9b4515ee631fddc63a2c8","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"Tennessee Titans","away_team":"Indianapolis Colts","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Indianapolis Colts","price":1.86},{"name":"Tennessee Titans","price":1.98}]}]}]},{"id":"ba1097486d1edb57bfe2bc22f5c4573e","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T17:01:00Z","home_team":"New Orleans Saints","away_team":"Tampa Bay Buccaneers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"New Orleans Saints","price":1.76},{"name":"Tampa Bay Buccaneers","price":2.12}]}]}]},{"id":"76fbc0191f917329bad82f76a9a22a2e","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T20:06:00Z","home_team":"Denver Broncos","away_team":"Los Angeles Chargers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Denver Broncos","price":2.1},{"name":"Los Angeles Chargers","price":1.77}]}]}]},{"id":"81df9672b5e68bc84e98641d5de2505b","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T20:06:00Z","home_team":"Las Vegas Raiders","away_team":"Pittsburgh Steelers","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Las Vegas Raiders","price":2.22},{"name":"Pittsburgh Steelers","price":1.69}]}]}]},{"id":"67c389265b00a40407a23054e45d8e45","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T20:26:00Z","home_team":"Carolina Panthers","away_team":"Atlanta Falcons","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Atlanta Falcons","price":1.6},{"name":"Carolina Panthers","price":2.4}]}]}]},{"id":"d4d2902446e120ea6f1afafdc0b3d55d","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-13T20:26:00Z","home_team":"Dallas Cowboys","away_team":"Detroit Lions","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Dallas Cowboys","price":2.2},{"name":"Detroit Lions","price":1.7}]}]}]},{"id":"245c50e05349966d749c7e3f05699647","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-14T00:21:00Z","home_team":"New York Giants","away_team":"Cincinnati Bengals","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Cincinnati Bengals","price":1.47},{"name":"New York Giants","price":2.8}]}]}]},{"id":"79b5655b7342104f50bc735a5d838b71","sport_key":"americanfootball_nfl","sport_title":"NFL","commence_time":"2024-10-15T00:16:00Z","home_team":"New York Jets","away_team":"Buffalo Bills","bookmakers":[{"key":"fanduel","title":"FanDuel","last_update":"2024-10-02T20:03:49Z","markets":[{"key":"h2h","last_update":"2024-10-02T20:03:49Z","outcomes":[{"name":"Buffalo Bills","price":1.79},{"name":"New York Jets","price":2.08}]}]}]}]

# Main Variables


def odds_converter(odd):
    if odd.is_integer():
        if odd > 0:
            return str("{:.2f}".format(round((odd / 100) + 1, 2)))
        else:
            return str("{:.2f}".format(round((100 / (odd * -1)) + 1, 2)))
    else:
        if odd > 2.00:
            return "+" + str(round((odd - 1) * 100))
        else:
            return str(round(-100 / (odd - 1)))


def date_converter(date):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%A %B %dth %Y")
    return formatted_date


def time_converter(time):
    if int(time[:2]) - 4 < 0:
        time = str(int(time[:2]) + 20) + time[2:]
    else:
        if int(time[:2]) - 4 < 10:
            time = "0" + str(int(time[:2]) - 4) + time[2:]
        else:
            time = str(int(time[:2]) - 4) + time[2:]

    if int(time[:2]) > 12:
        return str(int(time[:2]) - 12) + ":" + time[3:5] + "PM"
    else:
        return str(time[1:2]) + ":" + time[3:5] + "AM"


def extract_data(json_file):
    print(json_file[0])
    for i in range(len(json_file)):
        date_time = json_file[i]['commence_time']
        home_team = json_file[i]['home_team']
        away_team = json_file[i]['away_team']
        home_odds = json_file[i]['bookmakers'][0]['markets'][0]['outcomes'][0]['price']
        away_odds = json_file[i]['bookmakers'][0]['markets'][0]['outcomes'][1]['price']
        total_bet = 100

        print("\n" + home_team + " (" + odds_converter(home_odds) + ") vs. " + away_team + " (" + odds_converter(away_odds) + ")")
        print(date_converter(date_time[:10]) + " at " + time_converter(date_time[11:-1]))
        if arbitrage_calculator(home_odds, away_odds, total_bet):
            home_bet, away_bet, profit = arbitrage_calculator(home_odds, away_odds, total_bet)
            print("Bet $" + home_bet + "on s and $" )
        else:
            print("No Arbitrage Opportunity as the total inverse probability is " + str(round((1 / home_odds + 1 / away_odds)*100, 2)) + "%\n")


def arbitrage_calculator(h_odds, a_odds, total_bet):

    #h_odds =
    #a_odds =

    impl_prob = 1 / h_odds + 1 / a_odds

    if impl_prob < 1:
        home_bet = total_bet/(1 + h_odds/a_odds)
        away_bet = total_bet - home_bet
        profit = home_bet * h_odds - total_bet
        return home_bet, away_bet, profit
    else:
        return False


extract_data(response)