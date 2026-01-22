from app.db.base import Base
from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="events.id")
    market_type: Mapped[str] = mapped_column(nullable=False)
    period: Mapped[str] = mapped_column(nullable=False, default="full_game")
    line: Mapped[float] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False)

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
