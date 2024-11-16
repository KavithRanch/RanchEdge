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
