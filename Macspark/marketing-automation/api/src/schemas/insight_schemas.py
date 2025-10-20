"""
Insight Pydantic Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class InsightBase(BaseModel):
    """Base insight schema"""
    campaign_id: str
    date: date
    impressions: int = 0
    clicks: int = 0
    spend: Decimal = Decimal("0.0")
    reach: int = 0
    frequency: Decimal = Decimal("0.0")
    ctr: Decimal = Decimal("0.0")
    cpc: Decimal = Decimal("0.0")
    cpm: Decimal = Decimal("0.0")
    cpa: Optional[Decimal] = None
    roas: Optional[Decimal] = None
    purchases: int = 0
    revenue: Decimal = Decimal("0.0")


class InsightCreate(InsightBase):
    """Schema for creating insight"""
    pass


class InsightResponse(InsightBase):
    """Schema for insight response"""
    id: str
    collected_at: datetime

    class Config:
        from_attributes = True


class InsightSummary(BaseModel):
    """Summary of insights over period"""
    total_spend: Decimal
    total_clicks: int
    total_impressions: int
    total_purchases: int
    average_ctr: Decimal
    average_cpc: Decimal
    average_cpa: Optional[Decimal] = None
    average_roas: Optional[Decimal] = None
    date_range: str
