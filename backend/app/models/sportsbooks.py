from sqlalchemy import DateTime, func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Sportsbook(Base):
    __tablename__ = "sportsbooks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

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
