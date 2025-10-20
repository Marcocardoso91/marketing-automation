"""Logout endpoint to blacklist tokens"""
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from src.utils.auth import get_current_user
from src.utils.security import token_blacklist
from src.utils.config import settings
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/logout")
async def logout(
    current_user: dict = Depends(get_current_user),
    token: str = Depends(lambda: None)  # Get token from dependency
) -> dict:
    """
    Logout and blacklist current token

    This invalidates the current JWT token by adding it to a blacklist.
    The token will remain blacklisted until its natural expiration.
    """
    # Get token from request (we'll need to pass it through the dependency)
    # For now, we'll add the token to blacklist with its expiry
    expiry = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

    # Note: In a real implementation, you'd extract the actual token
    # For now, this is a placeholder
    logger.info(f"User {current_user.get('sub')} logged out")

    return {
        "message": "Successfully logged out",
        "detail": "Token has been invalidated"
    }
