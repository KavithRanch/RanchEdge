"""add sportsbooks timestamp server defaults

Revision ID: edfb2ab29d7b
Revises: a8b0740106e3
Create Date: 2026-01-26 20:10:23.842257

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "edfb2ab29d7b"
down_revision: Union[str, Sequence[str], None] = "a8b0740106e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "sportsbooks",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.text("now()"),
    )
    op.alter_column(
        "sportsbooks",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=sa.text("now()"),
    )


def downgrade():
    op.alter_column(
        "sportsbooks",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=None,
    )
    op.alter_column(
        "sportsbooks",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        server_default=None,
    )
