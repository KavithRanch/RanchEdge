"""
This module defines the TrueProbability model for this applciation
It represents the true probabilities of outcomes for a given market and odds snapshot.
It includes fields for the associate odds snapshot and market
It also includes fields for outcome name, outcome point, true probability, true probability calculation method, and the entry creation timestamp.
Its values are populated through the true_probability.py cli script which calculates true probabilities based on the ingested odds data and the selected calculation method for a given snapshot.

Author: Kavith Ranchagoda
Last Updated:
"""

from app.db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Numeric, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


class TrueProbability(Base):
    __tablename__ = "true_probabilities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    odds_snapshot_id: Mapped[int] = mapped_column(ForeignKey("odds_snapshots.id", ondelete="CASCADE"), nullable=False, index=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id", ondelete="CASCADE"), nullable=False, index=True)

    outcome_name: Mapped[str] = mapped_column(nullable=False)
    outcome_point: Mapped[float] = mapped_column(Numeric(8, 3), nullable=True)

    true_prob: Mapped[float] = mapped_column(Numeric(8, 6), nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)

    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "odds_snapshot_id",
            "market_id",
            "outcome_name",
            "outcome_point",
            "method",
            name="uq_snapshot_market_outcome_point_method",
        ),
        Index("ix_market_snapshot", "market_id", "odds_snapshot_id"),
    )
