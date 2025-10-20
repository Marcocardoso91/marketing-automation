"""
Audit Log SQLAlchemy Model
"""
from sqlalchemy import Column, String, JSON, DateTime, Index
from datetime import datetime
import uuid

from src.utils.database import Base


class AuditLog(Base):
    """Audit log for all system actions"""
    __tablename__ = "audit_log"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # CAMPAIGN_PAUSED, BUDGET_ADJUSTED, etc.
    action = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False)  # Campaign, Suggestion, etc.
    entity_id = Column(String, nullable=False, index=True)
    before_state = Column(JSON, nullable=True)  # State before action
    after_state = Column(JSON, nullable=True)  # State after action
    user_id = Column(String, nullable=True)  # Who triggered (if manual)
    metadata = Column(JSON, nullable=True)  # Additional context
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('idx_entity_timestamp', 'entity_type', 'entity_id', 'timestamp'),
    )

    def __repr__(self):
        return f"<AuditLog(action={self.action}, entity_type={self.entity_type}, entity_id={self.entity_id})>"
