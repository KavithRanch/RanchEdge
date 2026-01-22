from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_name: Mapped[str] = mapped_column(nullable=False)
    team_abv: Mapped[str] = mapped_column(nullable=False)

    league_id: Mapped[int] = mapped_column(ForeignKey("leagues.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

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
        UniqueConstraint("team_name", "league_id", name="uq_team_league"),
        UniqueConstraint("team_abv", "league_id", name="uq_teamabv_league"),
    )
