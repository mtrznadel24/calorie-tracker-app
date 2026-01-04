"""rename meals to meal_logs

Revision ID: 23b4f603688a
Revises: 54905e0df487
Create Date: 2025-12-31 00:53:10.394867

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "23b4f603688a"
down_revision: str | Sequence[str] | None = "54905e0df487"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f("ix_meals_date"), table_name="meals")
    op.drop_index(op.f("ix_meals_id"), table_name="meals")
    op.drop_index(op.f("ix_meals_name"), table_name="meals")
    op.drop_index(op.f("ix_meals_type"), table_name="meals")
    op.drop_index(op.f("ix_meals_user_id"), table_name="meals")
    op.drop_table("meals")

    op.execute("DROP TYPE IF EXISTS meal_type CASCADE")

    op.create_table(
        "meal_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "BREAKFAST", "LUNCH", "DINNER", "SNACK", "SUPPER", name="meal_type"
            ),
            nullable=False,
        ),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("calories", sa.Float(), nullable=False),
        sa.Column("proteins", sa.Float(), nullable=False),
        sa.Column("fats", sa.Float(), nullable=False),
        sa.Column("carbs", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meal_logs_date"), "meal_logs", ["date"], unique=False)
    op.create_index(op.f("ix_meal_logs_id"), "meal_logs", ["id"], unique=False)
    op.create_index(op.f("ix_meal_logs_name"), "meal_logs", ["name"], unique=False)
    op.create_index(op.f("ix_meal_logs_type"), "meal_logs", ["type"], unique=False)
    op.create_index(
        op.f("ix_meal_logs_user_id"), "meal_logs", ["user_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_meal_logs_user_id"), table_name="meal_logs")
    op.drop_index(op.f("ix_meal_logs_type"), table_name="meal_logs")
    op.drop_index(op.f("ix_meal_logs_name"), table_name="meal_logs")
    op.drop_index(op.f("ix_meal_logs_id"), table_name="meal_logs")
    op.drop_index(op.f("ix_meal_logs_date"), table_name="meal_logs")
    op.drop_table("meal_logs")

    op.execute("DROP TYPE IF EXISTS meal_type CASCADE")

    op.create_table(
        "meals",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("date", sa.DATE(), autoincrement=False, nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "BREAKFAST", "LUNCH", "DINNER", "SNACK", "SUPPER", name="meal_type"
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "weight",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "calories",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "proteins",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "fats",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "carbs",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("meals_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("meals_pkey")),
    )
    op.create_index(op.f("ix_meals_user_id"), "meals", ["user_id"], unique=False)
    op.create_index(op.f("ix_meals_type"), "meals", ["type"], unique=False)
    op.create_index(op.f("ix_meals_name"), "meals", ["name"], unique=False)
    op.create_index(op.f("ix_meals_id"), "meals", ["id"], unique=False)
    op.create_index(op.f("ix_meals_date"), "meals", ["date"], unique=False)
