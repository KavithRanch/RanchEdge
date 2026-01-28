SEED_SPORTS: list[str] = [
    "basketball",
    "football",
]


SEED_SPORTSBOOKS: list[tuple[str, str]] = [
    ("draftkings", "DraftKings"),
    ("fanduel", "FanDuel"),
    ("betmgm", "BetMGM"),
    ("betrivers", "BetRivers"),
    ("espnbet", "ESPN Bet"),
]
SPORTSBOOK_KEYS = [key for key, _ in SEED_SPORTSBOOKS]


SEED_LEAGUES: list[tuple[str, str, str]] = [
    ("nba", "basketball", "NBA"),
    ("nfl", "football", "NFL"),
]
LEAGUE_KEYS = [key for key, _, _ in SEED_LEAGUES]


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


DEFAULT_MARKETS = ["h2h", "spreads", "totals"]
