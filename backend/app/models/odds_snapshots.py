"""
This module defines the OddsSnapshot model for the application.
The OddsSnapshot model represents a snapshot of the odds data pulled from an external source at a specific point in time.
It includes fields for the source of the odds data, the timestamp when the data was pulled and the entry creation timestamp.
Its values are populated through the ingest_odds.py script when a call is made to an external apis.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.db.base import Base
from sqlalchemy import DateTime, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pulled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    source: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (Index("ix_source_pulledat", "source", "pulled_at"),)
