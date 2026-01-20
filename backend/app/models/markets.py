from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(not_null=True)
    market_type: Mapped[str] = mapped_column(not_null=True)
    period: Mapped[str] = mapped_column(not_null=True, default="full_game")
    line: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(not_null=True)
