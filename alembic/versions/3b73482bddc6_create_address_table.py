"""create address table

Revision ID: 3b73482bddc6
Revises: 3eb6d104b6f1
Create Date: 2026-01-23 15:59:33.122724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b73482bddc6'
down_revision: Union[str, Sequence[str], None] = '3eb6d104b6f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('address',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('address1', sa.String(),nullable=False),
                    sa.Column('address2', sa.String(),nullable=False),
                    sa.Column('city', sa.String(),nullable=False),
                    sa.Column('state', sa.String(),nullable=False),
                    sa.Column('country', sa.String(),nullable=False),
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('address')
