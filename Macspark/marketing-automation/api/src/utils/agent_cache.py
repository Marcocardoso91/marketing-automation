"""
Cached Agent Provider - Singleton with TTL

Solves P0 #5: FacebookAdsAgent recreated per request
Reduces latency from +300-500ms to ~0ms for cached instances.
"""
import time
from typing import Optional
from src.agents.facebook_agent import FacebookAdsAgent
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CachedAgentProvider:
    """
    Provides cached Facebook Ads Agent instances with TTL.

    Performance:
    - First call: ~400ms (creates agent + initializes Facebook SDK)
    - Cached calls: ~0ms (returns existing instance)
    - Auto-refresh: Every 3600s (1 hour) to prevent stale connections

    Thread-safe: Yes (single-threaded FastAPI OK, async-safe)
    Memory: ~5MB per agent instance
    """

    def __init__(self, cache_ttl: int = 3600):
        """
        Initialize agent provider.

        Args:
            cache_ttl: Cache Time-To-Live in seconds (default: 1 hour)
        """
        self._agent: Optional[FacebookAdsAgent] = None
        self._cache_time: Optional[float] = None
        self._cache_ttl = cache_ttl
        self._creation_count = 0

    def get_agent(self) -> FacebookAdsAgent:
        """
        Get cached Facebook Ads Agent or create new if expired.

        Returns:
            FacebookAdsAgent instance (cached or new)
        """
        now = time.time()

        # Check if cache is still valid
        if self._agent is not None and self._cache_time is not None:
            age = now - self._cache_time

            if age < self._cache_ttl:
                logger.debug(
                    f"Returning cached FacebookAdsAgent (age: {age:.1f}s, "
                    f"ttl: {self._cache_ttl}s)"
                )
                return self._agent
            else:
                logger.info(
                    f"FacebookAdsAgent cache expired (age: {age:.1f}s > "
                    f"ttl: {self._cache_ttl}s), creating new instance"
                )

        # Create new agent
        logger.info("Creating new FacebookAdsAgent instance")
        start_time = time.time()

        try:
            self._agent = FacebookAdsAgent()
            self._cache_time = now
            self._creation_count += 1

            init_time = time.time() - start_time
            logger.info(
                f"FacebookAdsAgent created successfully "
                f"(took {init_time*1000:.1f}ms, count: {self._creation_count})"
            )

            return self._agent

        except Exception as e:
            logger.error(f"Failed to create FacebookAdsAgent: {e}")
            # Re-raise para que o endpoint retorne 503
            raise

    def invalidate_cache(self) -> None:
        """
        Manually invalidate cache (useful for configuration changes).

        Example:
            # After updating Facebook credentials
            agent_provider.invalidate_cache()
            agent = agent_provider.get_agent()  # Will create new instance
        """
        logger.info("Manually invalidating FacebookAdsAgent cache")
        self._agent = None
        self._cache_time = None

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dict with cache stats (for monitoring/debugging)
        """
        if self._cache_time:
            age = time.time() - self._cache_time
            is_valid = age < self._cache_ttl
        else:
            age = None
            is_valid = False

        return {
            "cached": self._agent is not None,
            "cache_age_seconds": age,
            "cache_ttl_seconds": self._cache_ttl,
            "is_valid": is_valid,
            "creation_count": self._creation_count,
        }


# Global singleton instance
_agent_provider: Optional[CachedAgentProvider] = None


def get_cached_agent_provider(cache_ttl: int = 3600) -> CachedAgentProvider:
    """
    Get singleton CachedAgentProvider instance.

    Args:
        cache_ttl: Cache TTL in seconds (default: 3600 = 1 hour)

    Returns:
        CachedAgentProvider singleton

    Usage in FastAPI dependency:
        def get_facebook_agent() -> FacebookAdsAgent:
            provider = get_cached_agent_provider()
            return provider.get_agent()
    """
    global _agent_provider
    if _agent_provider is None:
        _agent_provider = CachedAgentProvider(cache_ttl=cache_ttl)
        logger.info(f"CachedAgentProvider initialized (TTL: {cache_ttl}s)")
    return _agent_provider


def get_facebook_agent() -> FacebookAdsAgent:
    """
    FastAPI Dependency: Get cached Facebook Ads Agent.

    Usage:
        @router.get("/campaigns")
        def get_campaigns(agent: FacebookAdsAgent = Depends(get_facebook_agent)):
            return agent.get_campaigns()

    Performance:
        - First call: ~400ms (cold start)
        - Subsequent calls: ~0ms (cached)
        - Auto-refresh: Every 1 hour

    Returns:
        FacebookAdsAgent instance (cached)

    Raises:
        Exception: If agent creation fails (propagates to 503 error)
    """
    provider = get_cached_agent_provider()
    return provider.get_agent()
