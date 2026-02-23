"""
This module defines the Event model for the application.
The Event model represents a sports event, such as a game or match, for which betting markets and odds are available.
It includes fields for the associated league, home and away teams, odds source information, start time and an entry creation timestamp.
Its values are populated through the ingest_odds.py script when processing the odds data from external apis.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.db.base import Base
from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"), nullable=False)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)

    source: Mapped[str] = mapped_column(nullable=False)
    source_event_id: Mapped[str] = mapped_column(nullable=False)

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("source", "source_event_id", name="uq_source_event"),
        Index("ix_league_starttime", "league_id", "start_time"),
        Index("ix_hometeam", "home_team_id"),
        Index("ix_awayteam", "away_team_id"),
    )
