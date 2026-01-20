from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    market_id: Mapped[str] = mapped_column(not_null=True)
    sportsbook_id: Mapped[int] = mapped_column(not_null=True)
    snapshot_id: Mapped[str] = mapped_column(not_null=True)

    american_odds: Mapped[float] = mapped_column(not_null=True)

    # Outcome identifiers
    # outcome_name: Team / Over / Under
    # outcome_point: Null / Point spread / Total points for O/U
    outcome_name: Mapped[str]
    outcome_point: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(not_null=True)
