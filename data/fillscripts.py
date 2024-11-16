import requests, os
from dotenv import load_dotenv
from backend import db, app
from backend.models import Team
load_dotenv()


def convert_team_data(team):
    if team['nbaComLogo1']:
        sport = "NBA"
        logo = "nbaComLogo1"
    elif team['nflComLogo1']:
        sport = "NFL"
        logo = "nflComLogo1"
    elif team['mlbLogo1']:
        sport = "MLB"
        logo = "mlbLogo1"
    else:
        sport = "NHL"
        logo = "espnLogo1"

    return {
        "id": team['teamID'],
        "sport_id": sport,
        "city": team['teamCity'],
        "name": team['teamName'],
        "logo": team[logo],
        "conference": team['conference'],
        "division": team['division'],
        "abbreviation": team['teamAbv']
    }


def get_teams_info():
    url = "https://tank01-fantasy-stats.p.rapidapi.com/getNBATeams"
    querystring = {"schedules":"false", "rosters":"false", "statsToGet":"averages", "topPerformers":"true", "teamStats":"true"}
    headers = {
        "x-rapidapi-key": f"{os.getenv('STATS_API_KEY')}",
        "x-rapidapi-host": "tank01-fantasy-stats.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_file = response.json()['body']

    if response.json()['statusCode']:
        with app.app_context():
            for team in json_file:
                team_data = convert_team_data(team)
                new_team = Team(**team_data)
                db.session.add(new_team)

            db.session.commit()



