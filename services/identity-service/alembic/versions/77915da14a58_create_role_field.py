"""create role field

Revision ID: 77915da14a58
Revises: 1b134eda844c
Create Date: 2026-07-21 16:46:16.609988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '77915da14a58'
down_revision: Union[str, Sequence[str], None] = '1b134eda844c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy.dialects import postgresql

user_role = postgresql.ENUM(
    "CUSTOMER",
    "RESTAURANT_OWNER",
    "DELIVERY_PARTNER",
    "ADMIN",
    name="user_role",
)

def upgrade():
    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="CUSTOMER",
        ),
    )


def downgrade():
    op.drop_column("users", "role")
    user_role.drop(op.get_bind(), checkfirst=True)