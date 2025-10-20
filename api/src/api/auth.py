"""Authentication endpoints"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    security,
    verify_password,
    verify_token,
)
from src.utils.database import get_async_session
from src.utils.security import password_validator
# Updated to use Redis-backed blacklist (P0 #3)
from src.utils.redis_blacklist import get_redis_blacklist
from src.utils.logger import setup_logger
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(session, login_data.email, login_data.password)
    if not user:
        logger.warning("Failed login attempt for %s", login_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.email})
    logger.info("User %s authenticated successfully", user.email)
    return LoginResponse(access_token=token)


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user.get("sub")}


@router.post("/change-password")
@limiter.limit("3/minute")
async def change_password(
    request: Request,
    old_password: str,
    new_password: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Change user password

    Validates password strength before changing.
    Rate limited to 3 attempts per minute.
    """
    is_valid, message = password_validator.validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)

    result = await session.execute(
        select(User).where(User.email == current_user.get("sub"))
    )
    user: Optional[User] = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.hashed_password = get_password_hash(new_password)
    await session.flush()

    # Revoke current token to enforce re-login
    payload = verify_token(credentials.credentials)
    expiry_ts = payload.get("exp")
    expiry_dt = datetime.utcfromtimestamp(expiry_ts) if expiry_ts else datetime.utcnow()
    blacklist = await get_redis_blacklist()
    await blacklist.add(credentials.credentials, expiry_dt)

    logger.info("Password changed for %s", user.email)

    return {
        "message": "Password changed successfully",
        "detail": "Please login again with your new password"
    }
