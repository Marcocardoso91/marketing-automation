"""Redis-based Token Blacklist - Production-ready implementation"""
import hashlib
from datetime import datetime
from typing import Optional
import redis.asyncio as redis
from src.utils.logger import setup_logger
from src.utils.config import settings

logger = setup_logger(__name__)


class RedisTokenBlacklist:
    """
    Production-ready token blacklist using Redis for persistence.

    Features:
    - Persists across server restarts
    - Automatic expiration via Redis TTL
    - Thread-safe and distributed-system ready
    - Async/await support

    Usage:
        blacklist = RedisTokenBlacklist()
        await blacklist.add(token, expiry)
        is_blacklisted = await blacklist.is_blacklisted(token)
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize Redis connection.

        Args:
            redis_url: Redis connection URL (defaults to settings.REDIS_URL)
        """
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis: Optional[redis.Redis] = None
        self._prefix = "token:blacklist:"

    async def _get_redis(self) -> redis.Redis:
        """Get or create Redis connection (lazy loading)"""
        if self._redis is None:
            try:
                self._redis = await redis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.info("Redis connection established for TokenBlacklist")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return self._redis

    async def add(self, token: str, expiry: datetime) -> None:
        """
        Add token to blacklist with automatic expiration.

        Args:
            token: JWT token to blacklist
            expiry: Token expiration time (used for TTL calculation)
        """
        try:
            # Hash token for privacy (don't store raw tokens)
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            key = f"{self._prefix}{token_hash}"

            # Calculate TTL in seconds
            now = datetime.utcnow()
            ttl = int((expiry - now).total_seconds())

            # Only add if TTL is positive
            if ttl > 0:
                r = await self._get_redis()
                await r.setex(key, ttl, "1")
                logger.info(
                    f"Token blacklisted with TTL {ttl}s (expires: {expiry})",
                    extra={"token_hash": token_hash[:16]}
                )
            else:
                logger.warning(
                    f"Token already expired (expiry: {expiry}), not adding to blacklist"
                )

        except Exception as e:
            logger.error(f"Error adding token to blacklist: {e}")
            # In production, decide: raise or fail silently?
            # For security, we raise to prevent tokens from being used
            raise

    async def is_blacklisted(self, token: str) -> bool:
        """
        Check if token is blacklisted.

        Args:
            token: JWT token to check

        Returns:
            True if blacklisted, False otherwise
        """
        try:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            key = f"{self._prefix}{token_hash}"

            r = await self._get_redis()
            exists = await r.exists(key)

            if exists:
                logger.warning(
                    f"Blacklisted token attempted to be used",
                    extra={"token_hash": token_hash[:16]}
                )

            return bool(exists)

        except Exception as e:
            logger.error(f"Error checking token blacklist: {e}")
            # Fail-secure: assume blacklisted if Redis is down
            return True

    async def remove(self, token: str) -> bool:
        """
        Remove token from blacklist (admin function).

        Args:
            token: JWT token to remove

        Returns:
            True if removed, False if not found
        """
        try:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            key = f"{self._prefix}{token_hash}"

            r = await self._get_redis()
            deleted = await r.delete(key)

            if deleted:
                logger.info(
                    f"Token removed from blacklist",
                    extra={"token_hash": token_hash[:16]}
                )

            return bool(deleted)

        except Exception as e:
            logger.error(f"Error removing token from blacklist: {e}")
            return False

    async def close(self) -> None:
        """Close Redis connection (call on shutdown)"""
        if self._redis:
            await self._redis.close()
            logger.info("Redis connection closed")


# Singleton instance for backward compatibility
_redis_blacklist: Optional[RedisTokenBlacklist] = None


async def get_redis_blacklist() -> RedisTokenBlacklist:
    """
    Get singleton Redis blacklist instance.

    Usage in FastAPI:
        blacklist = await get_redis_blacklist()
        await blacklist.add(token, expiry)
    """
    global _redis_blacklist
    if _redis_blacklist is None:
        _redis_blacklist = RedisTokenBlacklist()
    return _redis_blacklist


class HybridTokenBlacklist:
    """
    Hybrid blacklist that works in both sync and async contexts.
    
    TEMPORARY SOLUTION for gradual migration.
    Prefer using RedisTokenBlacklist directly with async/await.
    
    Usage (sync - deprecated):
        blacklist.add_sync(token, expiry)
        blacklist.is_blacklisted_sync(token)
    
    Usage (async - recommended):
        await blacklist.add(token, expiry)
        await blacklist.is_blacklisted(token)
    """
    
    def __init__(self):
        self._redis_blacklist = RedisTokenBlacklist()
        logger.warning(
            "Using HybridTokenBlacklist (sync wrapper). "
            "Migrate to async RedisTokenBlacklist for better performance."
        )
    
    def add_sync(self, token: str, expiry: datetime) -> None:
        """Synchronous add (uses asyncio.run - has overhead)"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # In async context - create task
                import nest_asyncio
                nest_asyncio.apply()
                loop.run_until_complete(self._redis_blacklist.add(token, expiry))
            else:
                asyncio.run(self._redis_blacklist.add(token, expiry))
        except Exception as e:
            logger.error(f"Sync add failed: {e}")
            raise
    
    def is_blacklisted_sync(self, token: str) -> bool:
        """Synchronous check (uses asyncio.run - has overhead)"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(
                    self._redis_blacklist.is_blacklisted(token)
                )
            else:
                return asyncio.run(self._redis_blacklist.is_blacklisted(token))
        except Exception as e:
            logger.error(f"Sync check failed: {e}")
            # Fail-secure: assume blacklisted
            return True
    
    async def add(self, token: str, expiry: datetime) -> None:
        """Async add (recommended)"""
        await self._redis_blacklist.add(token, expiry)
    
    async def is_blacklisted(self, token: str) -> bool:
        """Async check (recommended)"""
        return await self._redis_blacklist.is_blacklisted(token)


# Global instance for backward compatibility with sync code
token_blacklist_redis = HybridTokenBlacklist()
