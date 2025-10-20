"""Authentication utilities"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.config import settings
from src.utils.logger import setup_logger
# Updated to use Redis-backed blacklist (P0 #3)
from src.utils.redis_blacklist import token_blacklist_redis as token_blacklist

logger = setup_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    """Hash raw password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify raw password against stored hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:  # pragma: no cover - safety fallback for corrupted hashes
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + \
        (expires_delta or timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """Fetch user by email and validate credentials"""
    result = await session.execute(select(User).where(User.email == email))
    user: Optional[User] = result.scalar_one_or_none()

    if not user or not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def verify_token(token: str) -> dict:
    """Decode JWT token and ensure it hasn't been revoked"""
    if token_blacklist.is_blacklisted_sync(token):
        logger.warning("Attempt to use blacklisted token")
        raise HTTPException(status_code=401, detail="Token has been revoked")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        if payload.get("sub") is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """FastAPI dependency that validates bearer token"""
    return verify_token(credentials.credentials)
