from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(not_null=True)
    league_abv: Mapped[str] = mapped_column(not_null=True)

    sport_id: Mapped[int] = mapped_column(not_null=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(not_null=True)
