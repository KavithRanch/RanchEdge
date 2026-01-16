from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Sportsbook(Base):
    __tablename__ = "sportsbooks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow
    )
