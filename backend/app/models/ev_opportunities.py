"""
This module defines the EvOpportunity model for the application.
The EvOpportunity model represents an expected value (EV) betting opportunity identified in the ingested odds data.
It includes fields for the associated odds snapshot, price, true probability, event, market and sportsbook.
It also includes fields for the calculated EV per dollar, edge, whether it's a positive EV opportunity and entry creation timestamps.
Its values are populated through the ev_opportunities.py cli script which identifies EV opportunities based on the price and true probability data for a given snapshot.

Author: Kavith Ranchagoda
Last Updated:
"""

from datetime import datetime
from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    ForeignKey,
    Numeric,
    UniqueConstraint,
    func,
)

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class EvOpportunity(Base):
    __tablename__ = "ev_opportunities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    odds_snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("odds_snapshots.id", ondelete="CASCADE"),
        nullable=False,
    )
    price_id: Mapped[int] = mapped_column(
        ForeignKey("prices.id", ondelete="CASCADE"),
        nullable=False,
    )
    true_probability_id: Mapped[int] = mapped_column(
        ForeignKey("true_probabilities.id", ondelete="CASCADE"),
        nullable=False,
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    market_id: Mapped[int] = mapped_column(
        ForeignKey("markets.id", ondelete="CASCADE"),
        nullable=False,
    )
    sportsbook_id: Mapped[int] = mapped_column(
        ForeignKey("sportsbooks.id", ondelete="CASCADE"),
        nullable=False,
    )

    ev_per_dollar: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    edge: Mapped[float] = mapped_column(Numeric(10, 6), nullable=False)
    is_positive_ev: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "price_id",
            "true_probability_id",
            name="uq_price_trueprob",
        ),
        Index("ix_evopp_snapshot_ev", "odds_snapshot_id", "ev_per_dollar"),
        Index("ix_evopp_snapshot_book", "odds_snapshot_id", "sportsbook_id"),
    )
