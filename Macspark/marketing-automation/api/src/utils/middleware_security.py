"""Security middleware"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from src.utils.security import security_headers, request_validator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Validate request size
        try:
            request_validator.validate_request_size(request)
        except Exception as e:
            logger.warning(f"Request validation failed: {e}")
            return Response(
                content=str(e),
                status_code=413,
                headers=security_headers.get_headers()
            )

        # Process request
        response = await call_next(request)

        # Add security headers
        for header, value in security_headers.get_headers().items():
            response.headers[header] = value

        return response


class RateLimitLoggerMiddleware(BaseHTTPMiddleware):
    """Log rate limit violations"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Log rate limit violations
        if response.status_code == 429:
            client_ip = request.client.host if request.client else "unknown"
            logger.warning(
                f"Rate limit exceeded - IP: {client_ip}, "
                f"Path: {request.url.path}, "
                f"Method: {request.method}"
            )

        return response
