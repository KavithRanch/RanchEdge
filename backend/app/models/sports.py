from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Sports(Base):
    __tablename__ = "sports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(not_null=True)
    created_at: Mapped[datetime] = mapped_column(not_null=True)
