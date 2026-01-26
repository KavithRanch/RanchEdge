from app.db.base import Base
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    league_name: Mapped[str] = mapped_column(nullable=False)
    league_abv: Mapped[str] = mapped_column(nullable=False)

    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("league_name", "sport_id", name="uq_league_name_sport"),
        UniqueConstraint("league_abv", "sport_id", name="uq_leagueabv_sport"),
    )
