from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.leagues import League
from app.models.teams import Team

SEED_TEAMS: dict[str, list[tuple[str, str]]] = {
    "nba": [
        ("Atlanta Hawks", "ATL"),
        ("Boston Celtics", "BOS"),
        ("Brooklyn Nets", "BKN"),
        ("Charlotte Hornets", "CHA"),
        ("Chicago Bulls", "CHI"),
        ("Cleveland Cavaliers", "CLE"),
        ("Dallas Mavericks", "DAL"),
        ("Denver Nuggets", "DEN"),
        ("Detroit Pistons", "DET"),
        ("Golden State Warriors", "GSW"),
        ("Houston Rockets", "HOU"),
        ("Indiana Pacers", "IND"),
        ("Los Angeles Clippers", "LAC"),
        ("Los Angeles Lakers", "LAL"),
        ("Memphis Grizzlies", "MEM"),
        ("Miami Heat", "MIA"),
        ("Milwaukee Bucks", "MIL"),
        ("Minnesota Timberwolves", "MIN"),
        ("New Orleans Pelicans", "NOP"),
        ("New York Knicks", "NYK"),
        ("Oklahoma City Thunder", "OKC"),
        ("Orlando Magic", "ORL"),
        ("Philadelphia 76ers", "PHI"),
        ("Phoenix Suns", "PHX"),
        ("Portland Trail Blazers", "POR"),
        ("Sacramento Kings", "SAC"),
        ("San Antonio Spurs", "SAS"),
        ("Toronto Raptors", "TOR"),
        ("Utah Jazz", "UTA"),
        ("Washington Wizards", "WAS"),
    ],
    "nfl": [
        ("Arizona Cardinals", "ARI"),
        ("Atlanta Falcons", "ATL"),
        ("Baltimore Ravens", "BAL"),
        ("Buffalo Bills", "BUF"),
        ("Carolina Panthers", "CAR"),
        ("Chicago Bears", "CHI"),
        ("Cincinnati Bengals", "CIN"),
        ("Cleveland Browns", "CLE"),
        ("Dallas Cowboys", "DAL"),
        ("Denver Broncos", "DEN"),
        ("Detroit Lions", "DET"),
        ("Green Bay Packers", "GB"),
        ("Houston Texans", "HOU"),
        ("Indianapolis Colts", "IND"),
        ("Jacksonville Jaguars", "JAX"),
        ("Kansas City Chiefs", "KC"),
        ("Las Vegas Raiders", "LV"),
        ("Los Angeles Chargers", "LAC"),
        ("Los Angeles Rams", "LAR"),
        ("Miami Dolphins", "MIA"),
        ("Minnesota Vikings", "MIN"),
        ("New England Patriots", "NE"),
        ("New Orleans Saints", "NO"),
        ("New York Giants", "NYG"),
        ("New York Jets", "NYJ"),
        ("Philadelphia Eagles", "PHI"),
        ("Pittsburgh Steelers", "PIT"),
        ("San Francisco 49ers", "SF"),
        ("Seattle Seahawks", "SEA"),
        ("Tampa Bay Buccaneers", "TB"),
        ("Tennessee Titans", "TEN"),
        ("Washington Commanders", "WAS"),
    ],
}


def seed_teams(session: Session) -> None:
    with session.begin():
        for league_abv in SEED_TEAMS:
            league = session.execute(
                select(League).where(League.league_abv == league_abv)
            ).scalar_one_or_none()
            if league is None:
                raise ValueError(
                    f"League '{league_abv}' does not exist. Cannot seed teams."
                )

            for team_name, team_abbreviation in SEED_TEAMS[league_abv]:
                # Check if the team already exists
                select_team = select(Team).where(
                    Team.team_name == team_name, Team.league_id == league.id
                )
                team_exists = session.execute(select_team).scalar_one_or_none()

                if team_exists is None:
                    # Create and add the new team
                    new_team = Team(
                        team_name=team_name,
                        team_abv=team_abbreviation,
                        league_id=league.id,
                    )
                    session.add(new_team)
