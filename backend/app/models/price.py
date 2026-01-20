from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Price(Base):
    __tablename__ = "prices"

    market_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    sportsbook_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    snapshot_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    american_odds: Mapped[float]
