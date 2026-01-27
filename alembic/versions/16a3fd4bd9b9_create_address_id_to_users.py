"""create address id to users

Revision ID: 16a3fd4bd9b9
Revises: 3b73482bddc6
Create Date: 2026-01-23 16:17:15.685959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16a3fd4bd9b9'
down_revision: Union[str, Sequence[str], None] = '3b73482bddc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('address_id', sa.String(), nullable=True))
    op.create_foreign_key('address_user_fk', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('address_user_fk', table_name='users', type_='foreignkey')
    op.drop_column('users', 'address_id')
