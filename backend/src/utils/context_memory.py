"""
Gerenciamento de Contexto de Conversação
"""

from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy import select, desc, or_
from sqlalchemy.exc import SQLAlchemyError

from src.models.conversation import ConversationMemory
from src.models.user import User
from src.utils.database import AsyncSessionLocal
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ContextManager:
    def __init__(self, context_window: int = 10):
        self.context_window = context_window

    async def get_conversation_history(
        self,
        user_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Retrieve the most recent messages for a user"""
        fetch_limit = limit or self.context_window

        async with AsyncSessionLocal() as session:
            stmt = (
                select(ConversationMemory)
                .where(ConversationMemory.user_id == user_id)
                .order_by(desc(ConversationMemory.timestamp))
                .limit(fetch_limit)
            )
            result = await session.execute(stmt)
            records = result.scalars().all()

        # Retornar na ordem cronológica (mais antigo primeiro)
        history = [
            {
                "role": record.role,
                "message": record.message,
                "metadata": record.context_metadata or {},
                "timestamp": record.timestamp.isoformat(),
            }
            for record in reversed(records)
        ]

        return history

    async def add_message(
        self,
        user_id: str,
        role: str,
        message: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """Persist conversation message for a user"""
        metadata = metadata or {}

        async with AsyncSessionLocal() as session:
            user = await session.scalar(
                select(User).where(or_(User.id == user_id, User.email == user_id))
            )
            if not user:
                logger.warning(
                    "Conversation context not stored because user %s was not found",
                    user_id,
                )
                return False

            memory = ConversationMemory(
                user_id=user.id,
                session_id=session_id,
                role=role,
                message=message,
                context_metadata=metadata,
                timestamp=datetime.utcnow(),
            )

            session.add(memory)

            try:
                await session.commit()
                logger.debug(
                    "Context stored for user %s (%s)", user_id, session_id or "default"
                )
                return True
            except SQLAlchemyError as exc:  # pragma: no cover - defensive logging
                await session.rollback()
                logger.error("Erro ao salvar contexto: %s", exc)
                return False


_context_manager: Optional[ContextManager] = None


def get_context_manager() -> ContextManager:
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager
