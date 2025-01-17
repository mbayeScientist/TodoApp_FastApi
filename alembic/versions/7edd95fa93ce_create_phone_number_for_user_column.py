"""create phone number for user column

Revision ID: 7edd95fa93ce
Revises: 
Create Date: 2024-12-24 01:18:06.053982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7edd95fa93ce'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_nuber',sa.String(),nullable=True))


def downgrade() -> None:
    pass
