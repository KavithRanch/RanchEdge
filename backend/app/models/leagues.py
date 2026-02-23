"""
This module defines the League model for the application.
The League model represents a sports league (NBA, NFL, MLS, LaLiga etc.) that can be associated with sports, teams and events.
It includes fields for the league's name, abbreviation, associated sport, active status, and timestamps
Its values are seeded through the seed.py cli script.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.db.base import Base
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_name: Mapped[str] = mapped_column(nullable=False)
    league_abv: Mapped[str] = mapped_column(nullable=False)

    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("league_name", "sport_id", name="uq_league_name_sport"),
        UniqueConstraint("league_abv", "sport_id", name="uq_leagueabv_sport"),
    )
