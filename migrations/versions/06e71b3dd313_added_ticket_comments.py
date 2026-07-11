"""Added ticket comments

Revision ID: 06e71b3dd313
Revises: 1149eb875db0
"""

from alembic import op
import sqlalchemy as sa


revision = "06e71b3dd313"
down_revision = "1149eb875db0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "ticket_comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("created_by", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade():
    op.drop_table("ticket_comments")