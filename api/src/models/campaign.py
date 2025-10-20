"""
Campaign SQLAlchemy Model
"""
from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.utils.database import Base


class CampaignStatus(str, enum.Enum):
    """Campaign status enum"""
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"


class Campaign(Base):
    """Facebook Ads Campaign model"""
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True)  # Facebook Campaign ID
    name = Column(String, nullable=False)
    status = Column(Enum(CampaignStatus), nullable=False, index=True)
    objective = Column(String, nullable=True)
    daily_budget = Column(Numeric(10, 2), nullable=True)
    lifetime_budget = Column(Numeric(10, 2), nullable=True)
    created_time = Column(DateTime, nullable=True)
    updated_time = Column(DateTime, nullable=True)
    synced_at = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    # Relationships
    insights = relationship(
        "Insight", back_populates="campaign", cascade="all, delete-orphan")
    suggestions = relationship(
        "Suggestion", back_populates="campaign", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Campaign(id={self.id}, name={self.name}, status={self.status})>"
