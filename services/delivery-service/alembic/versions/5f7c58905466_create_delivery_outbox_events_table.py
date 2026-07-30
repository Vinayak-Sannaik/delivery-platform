"""create delivery outbox events table

Revision ID: 5f7c58905466
Revises: 3569a06ef8f4
Create Date: 2026-07-30 13:37:25.767590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5f7c58905466'
down_revision: Union[str, Sequence[str], None] = '3569a06ef8f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'outbox_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('aggregate_type', sa.String(length=100), nullable=False),
        sa.Column('aggregate_id', sa.UUID(), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='delivery'
    )

    op.create_index(
        'ix_delivery_outbox_status',
        'outbox_events',
        ['status'],
        unique=False,
        schema='delivery'
    )


def downgrade() -> None:
    op.drop_index(
        'ix_delivery_outbox_status',
        table_name='outbox_events',
        schema='delivery'
    )

    op.drop_table(
        'outbox_events',
        schema='delivery'
    )