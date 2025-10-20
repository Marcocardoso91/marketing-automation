-- Marketing Automation - Database Setup
-- Generated from Alembic migrations 001 + 002

-- Create ENUM types
CREATE TYPE campaignstatus AS ENUM ('ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED');
CREATE TYPE suggestiontype AS ENUM ('PAUSE', 'BUDGET_UP', 'BUDGET_DOWN', 'CREATIVE_REFRESH', 'AUDIENCE_EXPANSION');
CREATE TYPE suggestionstatus AS ENUM ('PENDING', 'ACCEPTED', 'REJECTED', 'APPLIED');

-- Create users table
CREATE TABLE users (
    id VARCHAR NOT NULL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    preferences JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ix_users_email ON users(email);

-- Create campaigns table
CREATE TABLE campaigns (
    id VARCHAR NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    status campaignstatus NOT NULL,
    objective VARCHAR,
    daily_budget NUMERIC(10,2),
    lifetime_budget NUMERIC(10,2),
    created_time TIMESTAMP,
    updated_time TIMESTAMP,
    synced_at TIMESTAMP
);

CREATE INDEX ix_campaigns_status ON campaigns(status);

-- Create insights table
CREATE TABLE insights (
    id VARCHAR NOT NULL PRIMARY KEY,
    campaign_id VARCHAR NOT NULL REFERENCES campaigns(id),
    date DATE NOT NULL,
    impressions INTEGER,
    clicks INTEGER,
    spend NUMERIC(10,2),
    reach INTEGER,
    frequency NUMERIC(5,2),
    ctr NUMERIC(5,2),
    cpc NUMERIC(10,2),
    cpm NUMERIC(10,2),
    cpa NUMERIC(10,2),
    roas NUMERIC(10,2),
    purchases INTEGER,
    revenue NUMERIC(10,2),
    collected_at TIMESTAMP
);

CREATE INDEX ix_insights_campaign_id ON insights(campaign_id);
CREATE INDEX ix_insights_date ON insights(date);
CREATE INDEX idx_campaign_date ON insights(campaign_id, date);

-- Create conversation_memory table
CREATE TABLE conversation_memory (
    id VARCHAR NOT NULL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    session_id VARCHAR,
    role VARCHAR NOT NULL,
    message TEXT NOT NULL,
    metadata JSON,
    timestamp TIMESTAMP
);

CREATE INDEX ix_conversation_memory_user_id ON conversation_memory(user_id);
CREATE INDEX ix_conversation_memory_session_id ON conversation_memory(session_id);
CREATE INDEX ix_conversation_memory_timestamp ON conversation_memory(timestamp);

-- Create suggestions table
CREATE TABLE suggestions (
    id VARCHAR NOT NULL PRIMARY KEY,
    campaign_id VARCHAR NOT NULL REFERENCES campaigns(id),
    type suggestiontype NOT NULL,
    reason VARCHAR NOT NULL,
    data JSON,
    status suggestionstatus DEFAULT 'PENDING',
    created_at TIMESTAMP,
    applied_at TIMESTAMP
);

CREATE INDEX ix_suggestions_campaign_id ON suggestions(campaign_id);
CREATE INDEX ix_suggestions_status ON suggestions(status);
CREATE INDEX idx_campaign_status ON suggestions(campaign_id, status);

-- Create audit_log table
CREATE TABLE audit_log (
    id VARCHAR NOT NULL PRIMARY KEY,
    action VARCHAR NOT NULL,
    entity_type VARCHAR NOT NULL,
    entity_id VARCHAR NOT NULL,
    before_state JSON,
    after_state JSON,
    user_id VARCHAR,
    metadata JSON,
    timestamp TIMESTAMP
);

CREATE INDEX ix_audit_log_action ON audit_log(action);
CREATE INDEX ix_audit_log_entity_id ON audit_log(entity_id);
CREATE INDEX ix_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_entity_timestamp ON audit_log(entity_type, entity_id, timestamp);

-- Create alembic_version table
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- Mark as migrated to version 002
INSERT INTO alembic_version (version_num) VALUES ('002_add_user_auth_fields');
