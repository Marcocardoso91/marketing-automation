"""
Suggestion Pydantic Schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SuggestionBase(BaseModel):
    """Base suggestion schema"""
    campaign_id: str
    type: str  # PAUSE, BUDGET_UP, BUDGET_DOWN, etc.
    reason: str
    data: Optional[Dict[str, Any]] = None


class SuggestionCreate(SuggestionBase):
    """Schema for creating suggestion"""
    pass


class SuggestionUpdate(BaseModel):
    """Schema for updating suggestion status"""
    status: str  # ACCEPTED, REJECTED, APPLIED


class SuggestionResponse(SuggestionBase):
    """Schema for suggestion response"""
    id: str
    status: str
    created_at: datetime
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True
