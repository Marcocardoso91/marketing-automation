"""
Campaign Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class CampaignBase(BaseModel):
    """Base campaign schema"""
    name: str
    status: str
    objective: Optional[str] = None
    daily_budget: Optional[Decimal] = None
    lifetime_budget: Optional[Decimal] = None


class CampaignCreate(CampaignBase):
    """Schema for creating campaign"""
    id: str


class CampaignUpdate(BaseModel):
    """Schema for updating campaign"""
    name: Optional[str] = None
    status: Optional[str] = None
    daily_budget: Optional[Decimal] = None
    lifetime_budget: Optional[Decimal] = None


class CampaignResponse(CampaignBase):
    """Schema for campaign response"""
    id: str
    created_time: Optional[datetime] = None
    updated_time: Optional[datetime] = None
    synced_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CampaignWithInsights(CampaignResponse):
    """Campaign with latest insights"""
    latest_spend: Optional[Decimal] = None
    latest_ctr: Optional[Decimal] = None
    latest_cpa: Optional[Decimal] = None
    latest_roas: Optional[Decimal] = None
