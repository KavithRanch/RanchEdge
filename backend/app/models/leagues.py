from app.db.base import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    league_abv: Mapped[str] = mapped_column(nullable=False)

    sport_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="sports.id")
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "sport_id", name="uq_name_sport"),
        UniqueConstraint("league_abv", "sport_id", name="uq_leagueabv_sport"),
    )
