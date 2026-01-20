from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sport_key: Mapped[str]
    home_team: Mapped[str]
    away_team: Mapped[str]
    start_time: Mapped[datetime]
