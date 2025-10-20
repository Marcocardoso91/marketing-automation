"""
Conversation Memory SQLAlchemy Model
"""
from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.utils.database import Base


class ConversationMemory(Base):
    """Conversation memory for AI context"""
    __tablename__ = "conversation_memory"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"),
                     nullable=False, index=True)
    session_id = Column(String, index=True, nullable=True)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    # Renamed from metadata (reserved word)
    context_metadata = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="conversations")

    def __repr__(self):
        return f"<ConversationMemory(user_id={self.user_id}, role={self.role})>"
