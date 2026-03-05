"""add_image_url_to_products_and_combo_items

Revision ID: b4e72c9d1f35
Revises: a3ba61a73b22
Create Date: 2026-03-05 21:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b4e72c9d1f35"
down_revision: str | None = "a3ba61a73b22"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "image_url",
            sa.Text(),
            nullable=True,
            comment="Base64-encoded product image (data URI).",
        ),
    )
    op.add_column(
        "combo_items",
        sa.Column(
            "image_url",
            sa.Text(),
            nullable=True,
            comment="Base64-encoded combo item image (data URI).",
        ),
    )


def downgrade() -> None:
    op.drop_column("combo_items", "image_url")
    op.drop_column("products", "image_url")
