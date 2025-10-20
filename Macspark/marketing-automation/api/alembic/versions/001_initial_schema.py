"""Initial schema

Revision ID: 001
Revises: 
Create Date: 2025-10-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_email', 'users', ['email'])

    # Create campaigns table
    op.create_table(
        'campaigns',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'PAUSED', 'DELETED',
                  'ARCHIVED', name='campaignstatus'), nullable=False),
        sa.Column('objective', sa.String(), nullable=True),
        sa.Column('daily_budget', sa.Numeric(10, 2), nullable=True),
        sa.Column('lifetime_budget', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_time', sa.DateTime(), nullable=True),
        sa.Column('updated_time', sa.DateTime(), nullable=True),
        sa.Column('synced_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_campaigns_status', 'campaigns', ['status'])

    # Create insights table
    op.create_table(
        'insights',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('campaign_id', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('impressions', sa.Integer(), nullable=True),
        sa.Column('clicks', sa.Integer(), nullable=True),
        sa.Column('spend', sa.Numeric(10, 2), nullable=True),
        sa.Column('reach', sa.Integer(), nullable=True),
        sa.Column('frequency', sa.Numeric(5, 2), nullable=True),
        sa.Column('ctr', sa.Numeric(5, 2), nullable=True),
        sa.Column('cpc', sa.Numeric(10, 2), nullable=True),
        sa.Column('cpm', sa.Numeric(10, 2), nullable=True),
        sa.Column('cpa', sa.Numeric(10, 2), nullable=True),
        sa.Column('roas', sa.Numeric(10, 2), nullable=True),
        sa.Column('purchases', sa.Integer(), nullable=True),
        sa.Column('revenue', sa.Numeric(10, 2), nullable=True),
        sa.Column('collected_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_insights_campaign_id', 'insights', ['campaign_id'])
    op.create_index('ix_insights_date', 'insights', ['date'])
    op.create_index('idx_campaign_date', 'insights', ['campaign_id', 'date'])

    # Create conversation_memory table
    op.create_table(
        'conversation_memory',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('session_id', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_conversation_memory_user_id',
                    'conversation_memory', ['user_id'])
    op.create_index('ix_conversation_memory_session_id',
                    'conversation_memory', ['session_id'])
    op.create_index('ix_conversation_memory_timestamp',
                    'conversation_memory', ['timestamp'])

    # Create suggestions table
    op.create_table(
        'suggestions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('campaign_id', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('PAUSE', 'BUDGET_UP', 'BUDGET_DOWN', 'CREATIVE_REFRESH',
                  'AUDIENCE_EXPANSION', name='suggestiontype'), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED',
                  'APPLIED', name='suggestionstatus'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('applied_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_suggestions_campaign_id',
                    'suggestions', ['campaign_id'])
    op.create_index('ix_suggestions_status', 'suggestions', ['status'])
    op.create_index('idx_campaign_status', 'suggestions',
                    ['campaign_id', 'status'])

    # Create audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('before_state', sa.JSON(), nullable=True),
        sa.Column('after_state', sa.JSON(), nullable=True),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_audit_log_action', 'audit_log', ['action'])
    op.create_index('ix_audit_log_entity_id', 'audit_log', ['entity_id'])
    op.create_index('ix_audit_log_timestamp', 'audit_log', ['timestamp'])
    op.create_index('idx_entity_timestamp', 'audit_log', [
                    'entity_type', 'entity_id', 'timestamp'])


def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('suggestions')
    op.drop_table('conversation_memory')
    op.drop_table('insights')
    op.drop_table('campaigns')
    op.drop_table('users')
