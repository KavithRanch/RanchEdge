from backend import db
from sqlalchemy import ForeignKey


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    city = db.Column(db.String(length=20), nullable=False)
    name = db.Column(db.String(length=20), nullable=False)
    logo = db.Column(db.String, nullable=False)
    conference = db.Column(db.String(length=7), nullable=False)
    division = db.Column(db.String(length=12), nullable=False)
    abbreviation = db.Column(db.String(length=3), nullable=False)


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    team_id = db.Column(db.Integer, ForeignKey('teams.id', ondelete="CASCADE"), nullable=False)
    position = db.Column(db.String(length=2), nullable=False)
    jersey_number = db.Column(db.Integer, nullable=False)
    height = db.Column(db.String(length=5), nullable=False)
    weight = db.Column(db.String(length=3), nullable=False)


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime(), nullable=False)
    referees = db.Column(db.ARRAY(db.Integer))
    home_team_id = db.Column(db.Integer, ForeignKey('teams.id', ondelete="CASCADE"), nullable=False)
    away_team_id = db.Column(db.Integer, ForeignKey('teams.id', ondelete="CASCADE"), nullable=False)
    game_type = db.Column(db.String(length=30))


class GameScores(db.Model):
    __tablename__ = "gamescores"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id', ondelete="CASCADE"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete="CASCADE"), nullable=False)
    period = db.Column(db.Integer, nullable=False)  # 1=Q1, 2=Q2, ..., OT1=5, OT2=6, etc.
    points = db.Column(db.Integer, nullable=False)


class NBAPlayerGameStats(db.Model):
    __tablename__ = "nbaplayergamestats"

    player_id = db.Column(db.Integer, ForeignKey('players.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, ForeignKey('games.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    minutes = db.Column(db.Integer(), nullable=False)
    points = db.Column(db.Integer(), nullable=False)
    field_goals_attempts = db.Column(db.Integer(), nullable=False)
    field_goals_made = db.Column(db.Integer(), nullable=False)
    three_points_attempts = db.Column(db.Integer(), nullable=False)
    three_points_made = db.Column(db.Integer(), nullable=False)
    free_throws_attempts = db.Column(db.Integer(), nullable=False)
    free_throws_made = db.Column(db.Integer(), nullable=False)
    assists = db.Column(db.Integer(), nullable=False)
    off_rebounds = db.Column(db.Integer(), nullable=False)
    def_rebounds = db.Column(db.Integer(), nullable=False)
    steals = db.Column(db.Integer(), nullable=False)
    blocks = db.Column(db.Integer(), nullable=False)
    turnovers = db.Column(db.Integer(), nullable=False)
    plus_minus = db.Column(db.Integer(), nullable=False)


class NBATeamGameStats(db.Model):
    __tablename__ = "nbateamgamestats"

    team_id = db.Column(db.Integer, ForeignKey('teams.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, ForeignKey('games.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    points = db.Column(db.Integer(), nullable=False)
    field_goals_attempts = db.Column(db.Integer(), nullable=False)
    field_goals_made = db.Column(db.Integer(), nullable=False)
    three_points_attempts = db.Column(db.Integer(), nullable=False)
    three_points_made = db.Column(db.Integer(), nullable=False)
    free_throws_attempts = db.Column(db.Integer(), nullable=False)
    free_throws_made = db.Column(db.Integer(), nullable=False)
    assists = db.Column(db.Integer(), nullable=False)
    off_rebounds = db.Column(db.Integer(), nullable=False)
    def_rebounds = db.Column(db.Integer(), nullable=False)
    steals = db.Column(db.Integer(), nullable=False)
    blocks = db.Column(db.Integer(), nullable=False)
    turnovers = db.Column(db.Integer(), nullable=False)
    plus_minus = db.Column(db.Integer(), nullable=False)


