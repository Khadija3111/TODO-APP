"""Initial migration for Conversation and Message tables

Revision ID: 001_conversation_message_tables
Revises:
Create Date: 2026-01-17 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = "001_conversation_message_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        "conversations",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("user_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversation_id"), "conversations", ["id"], unique=False)
    op.create_index(op.f("ix_conversation_user_id"), "conversations", ["user_id"], unique=False)

    # Create messages table
    op.create_table(
        "messages",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("conversation_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("role", sa.Enum("user", "assistant", name="messagerole"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tool_calls", sa.JSON(), nullable=True),
        sa.Column("tool_results", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_message_id"), "messages", ["id"], unique=False)
    op.create_index(op.f("ix_message_conversation_id"), "messages", ["conversation_id"], unique=False)


def downgrade() -> None:
    # Drop messages table
    op.drop_index(op.f("ix_message_conversation_id"), table_name="messages")
    op.drop_index(op.f("ix_message_id"), table_name="messages")
    op.drop_table("messages")

    # Drop conversations table
    op.drop_index(op.f("ix_conversation_user_id"), table_name="conversations")
    op.drop_index(op.f("ix_conversation_id"), table_name="conversations")
    op.drop_table("conversations")

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS messagerole")