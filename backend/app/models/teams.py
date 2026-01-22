from sqlalchemy import UniqueConstraint
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    team_name: Mapped[str] = mapped_column(nullable=False)
    team_abv: Mapped[str] = mapped_column(nullable=False)

    league_id: Mapped[int] = mapped_column(nullable=False, ForeignKey="leagues.id")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (
        UniqueConstraint("team_name", "league_id", name="uq_team_league"),
        UniqueConstraint("team_abv", "league_id", name="uq_teamabv_league"),
    )
