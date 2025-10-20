"""
FastAPI Middleware for metrics and monitoring
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from time import time
import uuid

from src.utils.metrics import api_requests_total, request_duration
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics"""

    async def dispatch(self, request: Request, call_next):
        # Generate correlation ID
        correlation_id = request.headers.get(
            "X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        # Start timer
        start_time = time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time() - start_time

        # Collect metrics
        api_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        request_duration.labels(
            endpoint=request.url.path
        ).observe(duration)

        # Add correlation ID to response
        response.headers["X-Correlation-ID"] = correlation_id

        # Log request
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s",
            extra={
                'correlation_id': correlation_id,
                'method': request.method,
                'path': request.url.path,
                'status': response.status_code,
                'duration': duration
            }
        )

        return response
