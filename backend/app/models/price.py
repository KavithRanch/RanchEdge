from app.db.base import Base
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    market_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="markets.id")
    sportsbook_id: Mapped[int] = mapped_column(
        nullable=False, ForeignKey="sportsbooks.id"
    )
    snapshot_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="snapshots.id")

    american_odds: Mapped[int] = mapped_column(nullable=False)

    # Outcome identifiers
    # outcome_name: Team / Over / Under
    # outcome_point: Null / Point spread / Total points for O/U
    outcome_name: Mapped[str] = mapped_column(nullable=False)
    outcome_point: Mapped[float] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "market_id",
            "sportsbook_id",
            "snapshot_id",
            "outcome_name",
            "outcome_point",
            name="uq_market_sportsbook_snapshot_outcome",
        ),
        Index("ix_market", "market_id"),
        Index("ix_sportsbook", "sportsbook_id"),
        Index("ix_snapshot", "snapshot_id"),
    )
