"""
Suggestion SQLAlchemy Model
"""
from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from src.utils.database import Base


class SuggestionType(str, enum.Enum):
    """Types of suggestions"""
    PAUSE = "PAUSE"
    BUDGET_UP = "BUDGET_UP"
    BUDGET_DOWN = "BUDGET_DOWN"
    CREATIVE_REFRESH = "CREATIVE_REFRESH"
    AUDIENCE_EXPANSION = "AUDIENCE_EXPANSION"


class SuggestionStatus(str, enum.Enum):
    """Suggestion workflow status"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    APPLIED = "APPLIED"


class Suggestion(Base):
    """AI-generated campaign suggestions"""
    __tablename__ = "suggestions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey(
        "campaigns.id"), nullable=False, index=True)
    type = Column(Enum(SuggestionType), nullable=False)
    reason = Column(String, nullable=False)  # Human-readable reasoning
    # Detailed data (current_ctr, threshold, etc.)
    data = Column(JSON, nullable=True)
    status = Column(Enum(SuggestionStatus),
                    default=SuggestionStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    applied_at = Column(DateTime, nullable=True)

    # Relationships
    campaign = relationship("Campaign", back_populates="suggestions")

    __table_args__ = (
        Index('idx_campaign_status', 'campaign_id', 'status'),
    )

    def __repr__(self):
        return f"<Suggestion(id={self.id}, type={self.type}, status={self.status})>"
