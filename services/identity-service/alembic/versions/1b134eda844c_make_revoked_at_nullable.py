"""make revoked_at nullable

Revision ID: 1b134eda844c
Revises: 02df427c1437
Create Date: 2026-07-16 11:38:20.491277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b134eda844c'
down_revision: Union[str, Sequence[str], None] = '02df427c1437'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "refresh_tokens",
        "revoked_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "refresh_tokens",
        "revoked_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
    )
