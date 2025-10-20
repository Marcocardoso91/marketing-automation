"""
Insight SQLAlchemy Model
"""
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.utils.database import Base


class Insight(Base):
    """Campaign Insights/Metrics model"""
    __tablename__ = "insights"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey(
        "campaigns.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # Metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    spend = Column(Numeric(10, 2), default=0.0)
    reach = Column(Integer, default=0)
    frequency = Column(Numeric(5, 2), default=0.0)

    # Calculated metrics
    ctr = Column(Numeric(5, 2), default=0.0)  # Click-through rate
    cpc = Column(Numeric(10, 2), default=0.0)  # Cost per click
    cpm = Column(Numeric(10, 2), default=0.0)  # Cost per mille
    cpa = Column(Numeric(10, 2), nullable=True)  # Cost per acquisition
    roas = Column(Numeric(10, 2), nullable=True)  # Return on ad spend

    # Conversions
    purchases = Column(Integer, default=0)
    revenue = Column(Numeric(10, 2), default=0.0)

    # Metadata
    collected_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", back_populates="insights")

    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_campaign_date', 'campaign_id', 'date'),
    )

    def __repr__(self):
        return f"<Insight(campaign_id={self.campaign_id}, date={self.date}, spend={self.spend})>"
