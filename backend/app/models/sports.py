"""
This module defines the Sport model for the application.
The Sport model represents a sport that can be associated with leagues.
It includes fields for the sport's name and timestamps.
Its values are seeded through the seed.py cli script.

Author: Kavith Ranchagoda
Last Updated:
"""

from sqlalchemy import DateTime, func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Sport(Base):
    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
