"""
Chat Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Schema for chat request"""
    message: str = Field(..., min_length=1, max_length=500)
    user_id: Optional[str] = "default_user"
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Schema for chat response"""
    type: str  # campaigns_list, performance_analysis, spend_analysis, general_info
    query: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistoryResponse(BaseModel):
    """Schema for conversation history"""
    role: str
    message: str
    metadata: Optional[Dict] = None
    timestamp: str
