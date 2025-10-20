"""
Cliente Facebook Graph API com retry e rate limiting.
Compartilhado entre serviços para evitar duplicação.
"""

import asyncio
import time
from typing import Any, Callable

from facebook_business.exceptions import FacebookRequestError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)


class RateLimitException(Exception):
    """Exceção levantada quando a API retorna erro de rate limit."""


class FacebookAPIClient:
    """Wrapper para chamadas à Facebook Marketing API com retry/backoff."""

    def __init__(self, max_retries: int = 5, backoff_base: float = 2.0):
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.request_count = 0
        self.last_request_time = 0.0

    def _check_rate_limit(self, error: FacebookRequestError) -> bool:
        """Verifica se o erro está relacionado a rate limit."""
        return error.api_error_code() in (17, 80004)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        retry=retry_if_exception_type(FacebookRequestError),
    )
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Executa chamada ao SDK com retry e controle de throughput."""
        try:
            current_time = time.time()
            if current_time - self.last_request_time < 0.1:
                await asyncio.sleep(0.1)

            self.request_count += 1
            self.last_request_time = time.time()

            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except FacebookRequestError as exc:
            if self._check_rate_limit(exc):
                raise RateLimitException(f"Rate limit: {exc.api_error_message()}") from exc
            raise


_facebook_api_client: FacebookAPIClient | None = None


def get_facebook_api_client() -> FacebookAPIClient:
    """Singleton compartilhado do cliente Facebook."""
    global _facebook_api_client
    if _facebook_api_client is None:
        _facebook_api_client = FacebookAPIClient()
    return _facebook_api_client
