from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    event_id: Mapped[int]
    market_key: Mapped[str]
    line: Mapped[str]
