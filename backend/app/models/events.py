from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_id: Mapped[int] = mapped_column(not_null=True)
    home_team_id: Mapped[int] = mapped_column(not_null=True)
    away_team_id: Mapped[int] = mapped_column(not_null=True)

    source: Mapped[str] = mapped_column(not_null=True)
    source_event_id: Mapped[int] = mapped_column(not_null=True)

    start_time: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(not_null=True)
