"""Added ticket activity timeline

Revision ID: 4b123caa279f
Revises: 06e71b3dd313
"""

from alembic import op
import sqlalchemy as sa


revision = "4b123caa279f"
down_revision = "06e71b3dd313"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ticket_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=255), nullable=False),
        sa.Column("performed_by", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("ticket_activities")