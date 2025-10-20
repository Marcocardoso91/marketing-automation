"""
Unit tests for custom exceptions.

Tests all 25 custom exception classes created in P1 #7.
"""

import pytest
from src.utils.exceptions import (
    # Base
    MarketingAutomationError,
    # Facebook
    FacebookAPIError,
    FacebookAuthenticationError,
    FacebookConnectionError,
    FacebookRateLimitError,
    FacebookDataError,
    # Database
    DatabaseError,
    DatabaseConnectionError,
    DatabaseQueryError,
    DatabaseMigrationError,
    # Agent
    AgentError,
    AgentInitializationError,
    AgentProcessingError,
    AgentCacheError,
    # Analytics
    AnalyticsError,
    AnalyticsCalculationError,
    AnalyticsDataError,
    AnomalyDetectionError,
    # Authentication
    AuthenticationError,
    InvalidTokenError,
    ExpiredTokenError,
    InvalidCredentialsError,
    TokenBlacklistedError,
    # Integration
    IntegrationError,
    NotionAPIError,
    N8NConnectionError,
    ExternalAPIError,
    # Automation
    AutomationError,
    CampaignOptimizationError,
    BudgetAllocationError,
    RuleExecutionError,
    # Helpers
    get_exception_for_context,
)


class TestBaseException:
    """Test MarketingAutomationError base class."""

    def test_basic_initialization(self):
        """Test basic exception creation."""
        error = MarketingAutomationError("Test error")

        assert error.message == "Test error"
        assert error.error_code == "MarketingAutomationError"
        assert error.details == {}

    def test_with_error_code(self):
        """Test exception with custom error code."""
        error = MarketingAutomationError(
            "Test error",
            error_code="CUSTOM_ERROR"
        )

        assert error.error_code == "CUSTOM_ERROR"

    def test_with_details(self):
        """Test exception with details."""
        details = {"key": "value", "count": 42}
        error = MarketingAutomationError(
            "Test error",
            details=details
        )

        assert error.details == details

    def test_to_dict(self):
        """Test conversion to dictionary."""
        error = MarketingAutomationError(
            "Test error",
            error_code="TEST_ERROR",
            details={"info": "test"}
        )

        result = error.to_dict()

        assert result == {
            "error": "TEST_ERROR",
            "message": "Test error",
            "details": {"info": "test"}
        }

    def test_str_representation(self):
        """Test string representation."""
        error = MarketingAutomationError("Test error")
        assert str(error) == "Test error"


class TestFacebookExceptions:
    """Test Facebook-related exceptions."""

    def test_facebook_api_error(self):
        """Test FacebookAPIError."""
        error = FacebookAPIError("API call failed")
        assert error.message == "API call failed"
        assert isinstance(error, MarketingAutomationError)

    def test_facebook_authentication_error(self):
        """Test FacebookAuthenticationError."""
        error = FacebookAuthenticationError()
        assert error.error_code == "FB_AUTH_ERROR"
        assert "authentication" in error.message.lower()

    def test_facebook_authentication_error_custom_message(self):
        """Test FacebookAuthenticationError with custom message."""
        error = FacebookAuthenticationError(
            "Invalid app secret",
            details={"app_id": "123456"}
        )
        assert error.message == "Invalid app secret"
        assert error.details["app_id"] == "123456"

    def test_facebook_connection_error(self):
        """Test FacebookConnectionError."""
        error = FacebookConnectionError()
        assert error.error_code == "FB_CONNECTION_ERROR"

    def test_facebook_rate_limit_error(self):
        """Test FacebookRateLimitError."""
        error = FacebookRateLimitError()
        assert error.error_code == "FB_RATE_LIMIT"

    def test_facebook_data_error(self):
        """Test FacebookDataError."""
        error = FacebookDataError()
        assert error.error_code == "FB_DATA_ERROR"


class TestDatabaseExceptions:
    """Test database-related exceptions."""

    def test_database_error(self):
        """Test DatabaseError."""
        error = DatabaseError("Query failed")
        assert isinstance(error, MarketingAutomationError)

    def test_database_connection_error(self):
        """Test DatabaseConnectionError."""
        error = DatabaseConnectionError()
        assert error.error_code == "DB_CONNECTION_ERROR"

    def test_database_query_error(self):
        """Test DatabaseQueryError."""
        error = DatabaseQueryError()
        assert error.error_code == "DB_QUERY_ERROR"

    def test_database_migration_error(self):
        """Test DatabaseMigrationError."""
        error = DatabaseMigrationError()
        assert error.error_code == "DB_MIGRATION_ERROR"


class TestAgentExceptions:
    """Test agent-related exceptions."""

    def test_agent_error(self):
        """Test AgentError."""
        error = AgentError("Agent failed")
        assert isinstance(error, MarketingAutomationError)

    def test_agent_initialization_error(self):
        """Test AgentInitializationError."""
        error = AgentInitializationError()
        assert error.error_code == "AGENT_INIT_ERROR"

    def test_agent_processing_error(self):
        """Test AgentProcessingError."""
        error = AgentProcessingError()
        assert error.error_code == "AGENT_PROCESSING_ERROR"

    def test_agent_cache_error(self):
        """Test AgentCacheError."""
        error = AgentCacheError()
        assert error.error_code == "AGENT_CACHE_ERROR"


class TestAnalyticsExceptions:
    """Test analytics-related exceptions."""

    def test_analytics_error(self):
        """Test AnalyticsError."""
        error = AnalyticsError("Calculation failed")
        assert isinstance(error, MarketingAutomationError)

    def test_analytics_calculation_error(self):
        """Test AnalyticsCalculationError."""
        error = AnalyticsCalculationError()
        assert error.error_code == "ANALYTICS_CALC_ERROR"

    def test_analytics_data_error(self):
        """Test AnalyticsDataError."""
        error = AnalyticsDataError()
        assert error.error_code == "ANALYTICS_DATA_ERROR"

    def test_anomaly_detection_error(self):
        """Test AnomalyDetectionError."""
        error = AnomalyDetectionError()
        assert error.error_code == "ANOMALY_DETECTION_ERROR"


class TestAuthenticationExceptions:
    """Test authentication-related exceptions."""

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, MarketingAutomationError)

    def test_invalid_token_error(self):
        """Test InvalidTokenError."""
        error = InvalidTokenError()
        assert error.error_code == "INVALID_TOKEN"

    def test_expired_token_error(self):
        """Test ExpiredTokenError."""
        error = ExpiredTokenError()
        assert error.error_code == "EXPIRED_TOKEN"

    def test_invalid_credentials_error(self):
        """Test InvalidCredentialsError."""
        error = InvalidCredentialsError()
        assert error.error_code == "INVALID_CREDENTIALS"

    def test_token_blacklisted_error(self):
        """Test TokenBlacklistedError."""
        error = TokenBlacklistedError()
        assert error.error_code == "TOKEN_BLACKLISTED"


class TestIntegrationExceptions:
    """Test integration-related exceptions."""

    def test_integration_error(self):
        """Test IntegrationError."""
        error = IntegrationError("API failed")
        assert isinstance(error, MarketingAutomationError)

    def test_notion_api_error(self):
        """Test NotionAPIError."""
        error = NotionAPIError()
        assert error.error_code == "NOTION_API_ERROR"

    def test_n8n_connection_error(self):
        """Test N8NConnectionError."""
        error = N8NConnectionError()
        assert error.error_code == "N8N_CONNECTION_ERROR"

    def test_external_api_error(self):
        """Test ExternalAPIError."""
        error = ExternalAPIError()
        assert error.error_code == "EXTERNAL_API_ERROR"


class TestAutomationExceptions:
    """Test automation-related exceptions."""

    def test_automation_error(self):
        """Test AutomationError."""
        error = AutomationError("Rule failed")
        assert isinstance(error, MarketingAutomationError)

    def test_campaign_optimization_error(self):
        """Test CampaignOptimizationError."""
        error = CampaignOptimizationError()
        assert error.error_code == "CAMPAIGN_OPT_ERROR"

    def test_budget_allocation_error(self):
        """Test BudgetAllocationError."""
        error = BudgetAllocationError()
        assert error.error_code == "BUDGET_ALLOC_ERROR"

    def test_rule_execution_error(self):
        """Test RuleExecutionError."""
        error = RuleExecutionError()
        assert error.error_code == "RULE_EXEC_ERROR"


class TestHelperFunctions:
    """Test helper functions."""

    def test_get_exception_for_context_facebook(self):
        """Test get_exception_for_context for Facebook."""
        exc_class = get_exception_for_context("facebook_api")
        assert exc_class == FacebookAPIError

    def test_get_exception_for_context_facebook_auth(self):
        """Test get_exception_for_context for Facebook auth."""
        exc_class = get_exception_for_context("facebook_auth")
        assert exc_class == FacebookAuthenticationError

    def test_get_exception_for_context_database(self):
        """Test get_exception_for_context for database."""
        exc_class = get_exception_for_context("database")
        assert exc_class == DatabaseError

    def test_get_exception_for_context_agent(self):
        """Test get_exception_for_context for agent."""
        exc_class = get_exception_for_context("agent")
        assert exc_class == AgentError

    def test_get_exception_for_context_analytics(self):
        """Test get_exception_for_context for analytics."""
        exc_class = get_exception_for_context("analytics")
        assert exc_class == AnalyticsError

    def test_get_exception_for_context_auth(self):
        """Test get_exception_for_context for auth."""
        exc_class = get_exception_for_context("auth")
        assert exc_class == AuthenticationError

    def test_get_exception_for_context_invalid_token(self):
        """Test get_exception_for_context for invalid token."""
        exc_class = get_exception_for_context("invalid_token")
        assert exc_class == InvalidTokenError

    def test_get_exception_for_context_unknown(self):
        """Test get_exception_for_context for unknown context."""
        exc_class = get_exception_for_context("unknown_context")
        assert exc_class == MarketingAutomationError


class TestExceptionInheritance:
    """Test exception inheritance hierarchy."""

    def test_facebook_exceptions_inherit_from_base(self):
        """Test Facebook exceptions inherit correctly."""
        assert issubclass(FacebookAuthenticationError, FacebookAPIError)
        assert issubclass(FacebookAPIError, MarketingAutomationError)

    def test_database_exceptions_inherit_from_base(self):
        """Test database exceptions inherit correctly."""
        assert issubclass(DatabaseConnectionError, DatabaseError)
        assert issubclass(DatabaseError, MarketingAutomationError)

    def test_agent_exceptions_inherit_from_base(self):
        """Test agent exceptions inherit correctly."""
        assert issubclass(AgentInitializationError, AgentError)
        assert issubclass(AgentError, MarketingAutomationError)

    def test_analytics_exceptions_inherit_from_base(self):
        """Test analytics exceptions inherit correctly."""
        assert issubclass(AnalyticsCalculationError, AnalyticsError)
        assert issubclass(AnalyticsError, MarketingAutomationError)

    def test_auth_exceptions_inherit_from_base(self):
        """Test auth exceptions inherit correctly."""
        assert issubclass(InvalidTokenError, AuthenticationError)
        assert issubclass(AuthenticationError, MarketingAutomationError)

    def test_integration_exceptions_inherit_from_base(self):
        """Test integration exceptions inherit correctly."""
        assert issubclass(NotionAPIError, IntegrationError)
        assert issubclass(IntegrationError, MarketingAutomationError)

    def test_automation_exceptions_inherit_from_base(self):
        """Test automation exceptions inherit correctly."""
        assert issubclass(CampaignOptimizationError, AutomationError)
        assert issubclass(AutomationError, MarketingAutomationError)


class TestExceptionCatching:
    """Test exception catching patterns."""

    def test_catch_specific_exception(self):
        """Test catching specific exception."""
        with pytest.raises(InvalidTokenError) as exc_info:
            raise InvalidTokenError("Token invalid")

        assert exc_info.value.error_code == "INVALID_TOKEN"

    def test_catch_base_exception(self):
        """Test catching base exception."""
        with pytest.raises(MarketingAutomationError):
            raise FacebookAuthenticationError()

    def test_catch_category_exception(self):
        """Test catching category exception."""
        with pytest.raises(FacebookAPIError):
            raise FacebookAuthenticationError()


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_api_error_response_format(self):
        """Test error formatting for API response."""
        error = FacebookAuthenticationError(
            "Authentication failed",
            details={
                "app_id": "123456",
                "account_id": "act_789",
                "timestamp": "2025-10-20T10:30:00Z"
            }
        )

        response = error.to_dict()

        assert response["error"] == "FB_AUTH_ERROR"
        assert "authentication" in response["message"].lower()
        assert response["details"]["app_id"] == "123456"
        assert "timestamp" in response["details"]

    def test_database_error_with_query_context(self):
        """Test database error with query context."""
        error = DatabaseQueryError(
            "Query execution failed",
            details={
                "query": "SELECT * FROM campaigns",
                "error": "Connection timeout"
            }
        )

        assert error.error_code == "DB_QUERY_ERROR"
        assert "query" in error.details
        assert error.details["error"] == "Connection timeout"

    def test_rate_limit_error_with_retry_info(self):
        """Test rate limit error with retry information."""
        error = FacebookRateLimitError(
            "Rate limit exceeded",
            details={
                "limit": 200,
                "remaining": 0,
                "reset_at": "2025-10-20T11:00:00Z"
            }
        )

        details = error.details
        assert details["limit"] == 200
        assert details["remaining"] == 0
        assert "reset_at" in details
