from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.sports import Sport

SEED_SPORTS: list[str] = [
    ("basketball"),
    ("football"),
]
