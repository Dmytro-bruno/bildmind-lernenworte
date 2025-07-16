"""restore words_total and add SM-2 fields to user_words

Revision ID: d9f40b01278e
Revises: 4a0ae6c0f3bb
Create Date: 2025-07-04 12:27:31.999415

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect  # <-- додаємо імпорт

# revision identifiers, used by Alembic.
revision: str = "d9f40b01278e"
down_revision: Union[str, None] = "4a0ae6c0f3bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Отримуємо актуальні колонки таблиці
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_cols = [c["name"] for c in inspector.get_columns("level_progress")]

    # Додаємо words_total тільки якщо його ще немає
    if "words_total" not in existing_cols:
        op.add_column(
            "level_progress",
            sa.Column("words_total", sa.Integer(), server_default=sa.text("0"), nullable=False),
        )

    op.add_column(
        "user_words",
        sa.Column("easiness_factor", sa.Float(), server_default=sa.text("2.5"), nullable=False),
    )
    op.add_column(
        "user_words",
        sa.Column("repetition", sa.Integer(), server_default=sa.text("0"), nullable=False),
    )
    op.add_column(
        "user_words",
        sa.Column("interval", sa.Integer(), server_default=sa.text("0"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_words", "interval")
    op.drop_column("user_words", "repetition")
    op.drop_column("user_words", "easiness_factor")
    op.drop_column("level_progress", "words_total")
