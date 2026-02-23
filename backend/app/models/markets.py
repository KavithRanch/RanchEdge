"""
This module defines the Market model for the application.
The Market model represents a betting market for a specific event, such as "Moneyline", "Spread", or "Total".
It includes fields for the associated event, betting market type, period, line and an entry creation timestamp.
Its fields are populated through the ingest_odds.py script when processing the odds data from external apis.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.db.base import Base
from sqlalchemy import DateTime, ForeignKey, Index, UniqueConstraint, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    market_type: Mapped[str] = mapped_column(nullable=False)
    period: Mapped[str] = mapped_column(nullable=False, default="full_game")
    line: Mapped[float] = mapped_column(Numeric(8, 3), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "market_type",
            "period",
            "line",
            name="uq_event_market_period_line",
        ),
        Index("ix_event", "event_id"),
    )
