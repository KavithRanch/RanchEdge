from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class OddsSnapshot(Base):
    __tablename__ = "odds_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pulled_at: Mapped[str]
    source: Mapped[str]
