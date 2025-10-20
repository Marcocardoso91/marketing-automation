"""
Custom Exception Hierarchy for Facebook Ads Marketing Automation API

Implements P1 #7: Replace 62 generic Exception handlers with specific exceptions.

Exception Hierarchy:
    MarketingAutomationError (base)
    ├── FacebookAPIError
    │   ├── FacebookAuthenticationError
    │   ├── FacebookConnectionError
    │   ├── FacebookRateLimitError
    │   └── FacebookDataError
    ├── DatabaseError
    │   ├── DatabaseConnectionError
    │   ├── DatabaseQueryError
    │   └── DatabaseMigrationError
    ├── AgentError
    │   ├── AgentInitializationError
    │   ├── AgentProcessingError
    │   └── AgentCacheError
    ├── AnalyticsError
    │   ├── AnalyticsCalculationError
    │   ├── AnalyticsDataError
    │   └── AnomalyDetectionError
    ├── AuthenticationError
    │   ├── InvalidTokenError
    │   ├── ExpiredTokenError
    │   ├── InvalidCredentialsError
    │   └── TokenBlacklistedError
    ├── IntegrationError
    │   ├── NotionAPIError
    │   ├── N8NConnectionError
    │   └── ExternalAPIError
    └── AutomationError
        ├── CampaignOptimizationError
        ├── BudgetAllocationError
        └── RuleExecutionError
"""

from typing import Optional, Dict, Any


# ============================================================================
# Base Exception
# ============================================================================

class MarketingAutomationError(Exception):
    """Base exception for all marketing automation errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }


# ============================================================================
# Facebook API Exceptions
# ============================================================================

class FacebookAPIError(MarketingAutomationError):
    """Base exception for Facebook API errors."""
    pass


class FacebookAuthenticationError(FacebookAPIError):
    """Raised when Facebook API authentication fails."""
    def __init__(self, message: str = "Facebook authentication failed", **kwargs):
        super().__init__(message, error_code="FB_AUTH_ERROR", **kwargs)


class FacebookConnectionError(FacebookAPIError):
    """Raised when connection to Facebook API fails."""
    def __init__(self, message: str = "Cannot connect to Facebook API", **kwargs):
        super().__init__(message, error_code="FB_CONNECTION_ERROR", **kwargs)


class FacebookRateLimitError(FacebookAPIError):
    """Raised when Facebook API rate limit is exceeded."""
    def __init__(self, message: str = "Facebook API rate limit exceeded", **kwargs):
        super().__init__(message, error_code="FB_RATE_LIMIT", **kwargs)


class FacebookDataError(FacebookAPIError):
    """Raised when Facebook API returns invalid or unexpected data."""
    def __init__(self, message: str = "Invalid data from Facebook API", **kwargs):
        super().__init__(message, error_code="FB_DATA_ERROR", **kwargs)


# ============================================================================
# Database Exceptions
# ============================================================================

class DatabaseError(MarketingAutomationError):
    """Base exception for database errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Raised when database connection fails."""
    def __init__(self, message: str = "Database connection failed", **kwargs):
        super().__init__(message, error_code="DB_CONNECTION_ERROR", **kwargs)


class DatabaseQueryError(DatabaseError):
    """Raised when database query execution fails."""
    def __init__(self, message: str = "Database query failed", **kwargs):
        super().__init__(message, error_code="DB_QUERY_ERROR", **kwargs)


class DatabaseMigrationError(DatabaseError):
    """Raised when database migration fails."""
    def __init__(self, message: str = "Database migration failed", **kwargs):
        super().__init__(message, error_code="DB_MIGRATION_ERROR", **kwargs)


# ============================================================================
# Agent Exceptions
# ============================================================================

class AgentError(MarketingAutomationError):
    """Base exception for agent-related errors."""
    pass


class AgentInitializationError(AgentError):
    """Raised when agent initialization fails."""
    def __init__(self, message: str = "Agent initialization failed", **kwargs):
        super().__init__(message, error_code="AGENT_INIT_ERROR", **kwargs)


class AgentProcessingError(AgentError):
    """Raised when agent processing fails."""
    def __init__(self, message: str = "Agent processing failed", **kwargs):
        super().__init__(message, error_code="AGENT_PROCESSING_ERROR", **kwargs)


class AgentCacheError(AgentError):
    """Raised when agent caching fails."""
    def __init__(self, message: str = "Agent cache error", **kwargs):
        super().__init__(message, error_code="AGENT_CACHE_ERROR", **kwargs)


# ============================================================================
# Analytics Exceptions
# ============================================================================

class AnalyticsError(MarketingAutomationError):
    """Base exception for analytics errors."""
    pass


class AnalyticsCalculationError(AnalyticsError):
    """Raised when analytics calculation fails."""
    def __init__(self, message: str = "Analytics calculation failed", **kwargs):
        super().__init__(message, error_code="ANALYTICS_CALC_ERROR", **kwargs)


class AnalyticsDataError(AnalyticsError):
    """Raised when analytics data is invalid."""
    def __init__(self, message: str = "Invalid analytics data", **kwargs):
        super().__init__(message, error_code="ANALYTICS_DATA_ERROR", **kwargs)


class AnomalyDetectionError(AnalyticsError):
    """Raised when anomaly detection fails."""
    def __init__(self, message: str = "Anomaly detection failed", **kwargs):
        super().__init__(message, error_code="ANOMALY_DETECTION_ERROR", **kwargs)


# ============================================================================
# Authentication Exceptions
# ============================================================================

class AuthenticationError(MarketingAutomationError):
    """Base exception for authentication errors."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when token is invalid."""
    def __init__(self, message: str = "Invalid token", **kwargs):
        super().__init__(message, error_code="INVALID_TOKEN", **kwargs)


class ExpiredTokenError(AuthenticationError):
    """Raised when token has expired."""
    def __init__(self, message: str = "Token has expired", **kwargs):
        super().__init__(message, error_code="EXPIRED_TOKEN", **kwargs)


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""
    def __init__(self, message: str = "Invalid credentials", **kwargs):
        super().__init__(message, error_code="INVALID_CREDENTIALS", **kwargs)


class TokenBlacklistedError(AuthenticationError):
    """Raised when token is blacklisted."""
    def __init__(self, message: str = "Token has been revoked", **kwargs):
        super().__init__(message, error_code="TOKEN_BLACKLISTED", **kwargs)


# ============================================================================
# Integration Exceptions
# ============================================================================

class IntegrationError(MarketingAutomationError):
    """Base exception for external integration errors."""
    pass


class NotionAPIError(IntegrationError):
    """Raised when Notion API call fails."""
    def __init__(self, message: str = "Notion API error", **kwargs):
        super().__init__(message, error_code="NOTION_API_ERROR", **kwargs)


class N8NConnectionError(IntegrationError):
    """Raised when N8N connection fails."""
    def __init__(self, message: str = "N8N connection failed", **kwargs):
        super().__init__(message, error_code="N8N_CONNECTION_ERROR", **kwargs)


class ExternalAPIError(IntegrationError):
    """Raised when external API call fails."""
    def __init__(self, message: str = "External API error", **kwargs):
        super().__init__(message, error_code="EXTERNAL_API_ERROR", **kwargs)


# ============================================================================
# Automation Exceptions
# ============================================================================

class AutomationError(MarketingAutomationError):
    """Base exception for automation errors."""
    pass


class CampaignOptimizationError(AutomationError):
    """Raised when campaign optimization fails."""
    def __init__(self, message: str = "Campaign optimization failed", **kwargs):
        super().__init__(message, error_code="CAMPAIGN_OPT_ERROR", **kwargs)


class BudgetAllocationError(AutomationError):
    """Raised when budget allocation fails."""
    def __init__(self, message: str = "Budget allocation failed", **kwargs):
        super().__init__(message, error_code="BUDGET_ALLOC_ERROR", **kwargs)


class RuleExecutionError(AutomationError):
    """Raised when automation rule execution fails."""
    def __init__(self, message: str = "Rule execution failed", **kwargs):
        super().__init__(message, error_code="RULE_EXEC_ERROR", **kwargs)


# ============================================================================
# Helper Functions
# ============================================================================

def get_exception_for_context(context: str) -> type[MarketingAutomationError]:
    """
    Get appropriate exception class for given context.

    Args:
        context: Error context (e.g., "facebook_api", "database", "agent")

    Returns:
        Exception class to use

    Examples:
        >>> get_exception_for_context("facebook_api")
        FacebookAPIError
        >>> get_exception_for_context("database")
        DatabaseError
    """
    context_map = {
        "facebook_api": FacebookAPIError,
        "facebook_auth": FacebookAuthenticationError,
        "facebook_connection": FacebookConnectionError,
        "facebook_rate_limit": FacebookRateLimitError,
        "facebook_data": FacebookDataError,
        "database": DatabaseError,
        "database_connection": DatabaseConnectionError,
        "database_query": DatabaseQueryError,
        "agent": AgentError,
        "agent_init": AgentInitializationError,
        "agent_processing": AgentProcessingError,
        "agent_cache": AgentCacheError,
        "analytics": AnalyticsError,
        "analytics_calculation": AnalyticsCalculationError,
        "analytics_data": AnalyticsDataError,
        "anomaly": AnomalyDetectionError,
        "auth": AuthenticationError,
        "invalid_token": InvalidTokenError,
        "expired_token": ExpiredTokenError,
        "invalid_credentials": InvalidCredentialsError,
        "token_blacklisted": TokenBlacklistedError,
        "integration": IntegrationError,
        "notion": NotionAPIError,
        "n8n": N8NConnectionError,
        "external_api": ExternalAPIError,
        "automation": AutomationError,
        "campaign_optimization": CampaignOptimizationError,
        "budget": BudgetAllocationError,
        "rule": RuleExecutionError,
    }

    return context_map.get(context, MarketingAutomationError)
