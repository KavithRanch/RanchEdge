from backend.app.db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Numeric, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


class TrueProbability(Base):
    __tablename__ = "true_probabilities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    odds_snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("odds_snapshots.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    market_id: Mapped[int] = mapped_column(
        ForeignKey("markets.id", ondelete="CASCADE"), nullable=False, index=True
    )

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
            name="uq_snapshot_market_outcome_point",
        ),
        Index("ix_market_snapshot", "market_id", "odds_snapshot_id"),
        Index("ix_event_snapshot", "event_id", "odds_snapshot_id"),
    )
