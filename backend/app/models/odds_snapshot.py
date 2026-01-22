from app.db.base import Base
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pulled_at: Mapped[datetime] = mapped_column(nullable=False)

    source: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    __table_args__ = (Index("ix_source_pulledat", "source", "pulled_at"),)
