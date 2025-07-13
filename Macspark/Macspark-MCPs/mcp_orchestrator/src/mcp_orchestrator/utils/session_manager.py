"""
Session Manager for Stateless MCP Orchestrator
----------------------------------------------
Gerencia sessões e estado usando Redis para permitir múltiplas réplicas stateless.
"""
import json
import uuid
import redis
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

log = logging.getLogger(__name__)

class Session(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_accessed: datetime
    metadata: Dict[str, Any] = {}
    conversation_history: list = []

class SessionManager:
    """Gerenciador de sessões stateless usando Redis"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", session_ttl: int = 3600):
        """
        Initialize session manager
        
        Args:
            redis_url: URL do Redis server
            session_ttl: TTL das sessões em segundos (default: 1 hora)
        """
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            log.info(f"Connected to Redis at {redis_url}")
        except redis.ConnectionError as e:
            log.warning(f"Redis connection failed: {e}. Fallback to memory storage.")
            self.redis_client = None
            self._memory_store = {}
        
        self.session_ttl = session_ttl
        self.session_prefix = "mcp_session:"
    
    def create_session(self, user_id: Optional[str] = None, metadata: Dict[str, Any] = None) -> str:
        """
        Criar nova sessão
        
        Args:
            user_id: ID do usuário (opcional)
            metadata: Metadados da sessão
            
        Returns:
            session_id: ID único da sessão
        """
        session_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            last_accessed=now,
            metadata=metadata or {},
            conversation_history=[]
        )
        
        self._store_session(session)
        log.info(f"Created session {session_id} for user {user_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Recuperar sessão por ID
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Session object ou None se não encontrada
        """
        if self.redis_client:
            try:
                session_data = self.redis_client.get(f"{self.session_prefix}{session_id}")
                if session_data:
                    data = json.loads(session_data)
                    session = Session(**data)
                    # Update last accessed
                    session.last_accessed = datetime.utcnow()
                    self._store_session(session)
                    return session
            except Exception as e:
                log.error(f"Error retrieving session {session_id}: {e}")
        else:
            # Fallback to memory
            return self._memory_store.get(session_id)
        
        return None
    
    def update_session(self, session_id: str, **updates) -> bool:
        """
        Atualizar sessão existente
        
        Args:
            session_id: ID da sessão
            **updates: Campos a serem atualizados
            
        Returns:
            bool: True se atualizada com sucesso
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Update fields
        for key, value in updates.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        session.last_accessed = datetime.utcnow()
        self._store_session(session)
        return True
    
    def add_to_conversation(self, session_id: str, message: Dict[str, Any]) -> bool:
        """
        Adicionar mensagem ao histórico da conversa
        
        Args:
            session_id: ID da sessão
            message: Mensagem a ser adicionada
            
        Returns:
            bool: True se adicionada com sucesso
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        message["timestamp"] = datetime.utcnow().isoformat()
        session.conversation_history.append(message)
        
        # Limit conversation history (keep last 100 messages)
        if len(session.conversation_history) > 100:
            session.conversation_history = session.conversation_history[-100:]
        
        session.last_accessed = datetime.utcnow()
        self._store_session(session)
        return True
    
    def delete_session(self, session_id: str) -> bool:
        """
        Deletar sessão
        
        Args:
            session_id: ID da sessão
            
        Returns:
            bool: True se deletada com sucesso
        """
        if self.redis_client:
            try:
                result = self.redis_client.delete(f"{self.session_prefix}{session_id}")
                log.info(f"Deleted session {session_id}")
                return result > 0
            except Exception as e:
                log.error(f"Error deleting session {session_id}: {e}")
        else:
            # Fallback to memory
            if session_id in self._memory_store:
                del self._memory_store[session_id]
                return True
        
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Limpar sessões expiradas (apenas para fallback memory)
        
        Returns:
            int: Número de sessões removidas
        """
        if self.redis_client:
            # Redis handles TTL automatically
            return 0
        
        # Manual cleanup for memory store
        cutoff = datetime.utcnow() - timedelta(seconds=self.session_ttl)
        expired_sessions = [
            sid for sid, session in self._memory_store.items()
            if session.last_accessed < cutoff
        ]
        
        for session_id in expired_sessions:
            del self._memory_store[session_id]
        
        log.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return len(expired_sessions)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Obter estatísticas das sessões
        
        Returns:
            Dict com estatísticas
        """
        if self.redis_client:
            try:
                pattern = f"{self.session_prefix}*"
                keys = self.redis_client.keys(pattern)
                return {
                    "total_sessions": len(keys),
                    "storage_type": "redis",
                    "redis_connected": True
                }
            except Exception:
                return {
                    "total_sessions": 0,
                    "storage_type": "redis",
                    "redis_connected": False
                }
        else:
            return {
                "total_sessions": len(self._memory_store),
                "storage_type": "memory",
                "redis_connected": False
            }
    
    def _store_session(self, session: Session) -> None:
        """Store session in Redis or memory fallback"""
        if self.redis_client:
            try:
                session_data = session.model_dump(mode='json')
                # Convert datetime objects to ISO strings
                session_data['created_at'] = session.created_at.isoformat()
                session_data['last_accessed'] = session.last_accessed.isoformat()
                
                self.redis_client.setex(
                    f"{self.session_prefix}{session.session_id}",
                    self.session_ttl,
                    json.dumps(session_data, default=str)
                )
            except Exception as e:
                log.error(f"Error storing session {session.session_id}: {e}")
                # Fallback to memory
                self._memory_store[session.session_id] = session
        else:
            # Store in memory
            self._memory_store[session.session_id] = session