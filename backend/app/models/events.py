from app.db.base import Base
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="leagues.id")
    home_team_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="teams.id")
    away_team_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="teams.id")

    source: Mapped[str] = mapped_column(nullable=False)
    source_event_id: Mapped[str] = mapped_column(nullable=False)

    start_time: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("source", "source_event_id", name="uq_source_event"),
        Index("ix_league_starttime", "league_id", "start_time"),
        Index("ix_hometeam", "home_team_id"),
        Index("ix_awayteam", "away_team_id"),
    )
