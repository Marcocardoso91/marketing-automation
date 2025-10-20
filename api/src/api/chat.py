"""
Chat API Router
Interface conversacional para queries em linguagem natural
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional

from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_cached_agent_provider
from src.schemas.chat_schemas import ChatRequest, ChatResponse, ConversationHistoryResponse
from src.utils.context_memory import get_context_manager
from src.utils.logger import setup_logger
from src.utils.auth import get_current_user
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat(
    request: Request,
    payload: ChatRequest,
    current_user: dict = Depends(get_current_user)
) -> ChatResponse:
    """
    Process natural language query

    Args:
        payload: Chat request with message and user_id
        current_user: Authenticated user payload

    Returns:
        Structured response with type and data
    """
    try:
        user_identifier = current_user.get("sub")
        if payload.user_id and payload.user_id != user_identifier:
            raise HTTPException(
                status_code=403,
                detail="You can only send messages on behalf of your own account"
            )

        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        context_manager = get_context_manager()

        # Save user message
        await context_manager.add_message(
            user_id=user_identifier,
            role="user",
            message=payload.message,
            session_id=payload.session_id
        )

        # Process query
        response = await agent.process_natural_language_query(payload.message)

        # Save assistant response
        await context_manager.add_message(
            user_id=user_identifier,
            role="assistant",
            message=str(response.get('data')),
            session_id=payload.session_id,
            metadata={'response_type': response['type']}
        )

        logger.info("Processed chat query from user %s", user_identifier)
        return ChatResponse(**response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[ConversationHistoryResponse])
@limiter.limit("20/minute")
async def get_chat_history(
    request: Request,
    user_id: Optional[str] = None,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
) -> List[ConversationHistoryResponse]:
    """
    Get conversation history for a user

    Args:
        user_id: Optional user identifier (defaults to authenticated user)
        limit: Maximum messages to return

    Returns:
        List of conversation messages
    """
    try:
        effective_user = current_user.get("sub")
        if user_id and user_id != effective_user:
            raise HTTPException(
                status_code=403,
                detail="You can only access your own conversation history"
            )

        context_manager = get_context_manager()
        history = await context_manager.get_conversation_history(
            effective_user,
            limit=limit
        )

        return history

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
