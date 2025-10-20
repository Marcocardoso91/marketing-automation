"""
Facebook Ads AI Agent - Main Application
FastAPI application entry point
"""
from src.api.metrics import limiter as metrics_limiter
from src.api import campaigns, analytics, automation, chat, notion, n8n_admin, auth, metrics
from src.utils.middleware import MetricsMiddleware
from src.utils.middleware_security import SecurityHeadersMiddleware, RateLimitLoggerMiddleware
from src.utils.rate_limit import limiter, RateLimitExceeded, _rate_limit_exceeded_handler
from slowapi import _rate_limit_exceeded_handler as slowapi_handler
from slowapi.errors import RateLimitExceeded as SlowAPIRateLimitExceeded
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from prometheus_client import make_asgi_app
from contextlib import asynccontextmanager

from src.utils.config import settings
from src.utils.logger import setup_logger
from src.utils.database import init_db, close_db

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down application")
    await close_db()


# FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered performance advisor for Facebook Ads campaigns",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware - Secure configuration
allowed_origins = settings.get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)

# Security middleware (order matters - first to last)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitLoggerMiddleware)

# Trusted hosts (prevent host header attacks)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.get_trusted_hosts()
    )

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# SlowAPI rate limiting (para endpoint de métricas)
app.state.metrics_limiter = metrics_limiter
app.add_exception_handler(SlowAPIRateLimitExceeded, slowapi_handler)

# Metrics middleware
app.add_middleware(MetricsMiddleware)

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Import and include routers

app.include_router(
    campaigns.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(
    analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(automation.router,
                   prefix="/api/v1/automation", tags=["Automation"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(notion.router, prefix="/api/v1/notion",
                   tags=["Notion Integration"])
app.include_router(n8n_admin.router, prefix="/api/v1/n8n",
                   tags=["n8n Management"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    metrics.router,
    prefix="/api/v1/metrics",
    tags=["Metrics Export"]
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"{settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
