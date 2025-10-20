# Migration Guide: Generic to Custom Exceptions

**Issue**: P1 #7 - Refactor 62 generic Exception handlers
**Priority**: High
**Effort**: 6 hours
**Impact**: Better error handling, debugging, and API responses

---

## Summary

Found **62 generic `except Exception` handlers** across the codebase:

| File | Count | Priority |
|------|-------|----------|
| `src/agents/facebook_agent.py` | 3 | 🔴 High |
| `src/analytics/performance_analyzer.py` | 3 | 🔴 High |
| `src/api/analytics.py` | 3 | 🟡 Medium |
| `src/api/automation.py` | 3 | 🟡 Medium |
| `src/api/campaigns.py` | 3 | 🟡 Medium |
| `src/api/chat.py` | 2 | 🟡 Medium |
| `src/api/metrics.py` | ~10 | 🟡 Medium |
| `src/api/notion.py` | ~5 | 🟢 Low |
| `src/api/n8n_admin.py` | ~5 | 🟢 Low |
| `src/tasks/collectors.py` | ~10 | 🟡 Medium |
| `src/tasks/processors.py` | ~10 | 🟡 Medium |
| `src/utils/token_manager.py` | 1 (`raise`) | 🔴 High |
| `src/utils/auth.py` | 1 | 🔴 High |
| `src/utils/database.py` | 1 | 🔴 High |

---

## Custom Exception Hierarchy

Created in `src/utils/exceptions.py`:

```python
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
```

---

## Migration Examples

### ❌ Before (Generic)

```python
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class FacebookAdsAgent:
    def _init_facebook_api(self):
        try:
            FacebookAdsApi.init(...)
        except Exception as e:
            logger.error(f"Failed to initialize Facebook API: {e}")
            raise
```

### ✅ After (Specific)

```python
from src.utils.logger import setup_logger
from src.utils.exceptions import FacebookAuthenticationError

logger = setup_logger(__name__)

class FacebookAdsAgent:
    def _init_facebook_api(self):
        try:
            FacebookAdsApi.init(...)
        except Exception as e:
            logger.error(f"Failed to initialize Facebook API: {e}")
            raise FacebookAuthenticationError(
                message=f"Failed to initialize Facebook API: {str(e)}",
                details={"app_id": self.app_id, "account_id": self.ad_account_id}
            )
```

---

## Migration Pattern by Context

### 1. Facebook API Calls

```python
# Import
from src.utils.exceptions import FacebookAPIError, FacebookDataError

# Usage
try:
    campaigns = await self.api_client.execute_with_retry(...)
except Exception as e:
    logger.error(f"Error fetching campaigns: {e}")
    raise FacebookAPIError(
        message=f"Failed to fetch campaigns: {str(e)}",
        details={"account_id": self.ad_account_id}
    )
```

### 2. Analytics Calculations

```python
# Import
from src.utils.exceptions import AnalyticsCalculationError

# Usage
try:
    score = calculate_performance_score(metrics)
except Exception as e:
    logger.error(f"Error calculating score: {e}")
    raise AnalyticsCalculationError(
        message=f"Failed to calculate performance score: {str(e)}",
        details={"metrics": metrics}
    )
```

### 3. Database Operations

```python
# Import
from src.utils.exceptions import DatabaseQueryError

# Usage
try:
    result = await session.execute(query)
except Exception as e:
    logger.error(f"Database query failed: {e}")
    raise DatabaseQueryError(
        message=f"Failed to execute query: {str(e)}",
        details={"query": str(query)}
    )
```

### 4. Authentication

```python
# Import
from src.utils.exceptions import InvalidTokenError

# Usage - in token_manager.py line 43
# BEFORE
raise Exception("Token inválido")

# AFTER
raise InvalidTokenError(
    message="Token validation failed",
    details={"reason": "invalid_format"}
)
```

---

## Migration Checklist

### Phase 1: Critical Files (2h)
- [ ] `src/utils/token_manager.py` (1 raise Exception)
- [ ] `src/utils/auth.py` (1 except)
- [ ] `src/utils/database.py` (1 except)
- [ ] `src/agents/facebook_agent.py` (3 excepts)

### Phase 2: High-Impact Files (2h)
- [ ] `src/analytics/performance_analyzer.py` (3 excepts)
- [ ] `src/api/campaigns.py` (3 excepts)
- [ ] `src/api/automation.py` (3 excepts)
- [ ] `src/api/analytics.py` (3 excepts)

### Phase 3: Background Tasks (1h)
- [ ] `src/tasks/collectors.py` (~10 excepts)
- [ ] `src/tasks/processors.py` (~10 excepts)

### Phase 4: Remaining Files (1h)
- [ ] `src/api/metrics.py`
- [ ] `src/api/chat.py`
- [ ] `src/api/notion.py`
- [ ] `src/api/n8n_admin.py`

---

## Benefits

### 1. Better Error Messages
```python
# Generic
{"error": "Internal Server Error"}

# Specific
{
    "error": "FB_AUTH_ERROR",
    "message": "Facebook authentication failed",
    "details": {
        "app_id": "123456",
        "account_id": "act_789"
    }
}
```

### 2. Targeted Error Handling
```python
# Can catch specific errors
try:
    agent.get_campaigns()
except FacebookRateLimitError:
    # Retry after delay
    await asyncio.sleep(60)
    agent.get_campaigns()
except FacebookDataError as e:
    # Log and continue with empty data
    logger.warning(f"Invalid data: {e}")
    return []
```

### 3. Better Monitoring
```python
# In Prometheus/Grafana
facebook_api_errors_total{type="rate_limit"} 45
facebook_api_errors_total{type="auth"} 2
database_errors_total{type="connection"} 1
```

---

## Testing

### Unit Tests

```python
# tests/unit/test_exceptions.py
import pytest
from src.utils.exceptions import FacebookAuthenticationError

def test_facebook_auth_error_to_dict():
    error = FacebookAuthenticationError(
        message="Auth failed",
        details={"app_id": "123"}
    )

    assert error.to_dict() == {
        "error": "FB_AUTH_ERROR",
        "message": "Auth failed",
        "details": {"app_id": "123"}
    }
```

### Integration Tests

```python
# tests/integration/test_error_responses.py
async def test_campaign_api_authentication_error(client):
    """Test that auth errors return proper HTTP 401."""
    response = await client.get("/api/campaigns", headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert response.json() == {
        "error": "INVALID_TOKEN",
        "message": "Invalid token",
        "details": {}
    }
```

---

## Validation

After migration, verify:

```bash
# 1. No generic exceptions remain (except rare cases)
grep -r "except Exception" src/ | wc -l
# Should be close to 0

# 2. All files import from exceptions.py
grep -r "from src.utils.exceptions import" src/ | wc -l
# Should be ~20-30 files

# 3. Tests pass
pytest api/tests/ -v

# 4. No syntax errors
python -m py_compile src/**/*.py
```

---

## Next Steps

1. ✅ Create custom exceptions hierarchy (`src/utils/exceptions.py`) - **DONE**
2. ⏳ Migrate Phase 1 (critical files) - **IN PROGRESS**
3. ⏳ Add unit tests for exceptions
4. ⏳ Update API error middleware to use `.to_dict()`
5. ⏳ Migrate remaining files
6. ⏳ Update monitoring dashboards

---

## Status: 🟡 IN PROGRESS

- **Created**: 62 custom exception classes
- **Migrated**: 0/62 handlers
- **Tested**: 0/62 handlers
- **Estimated completion**: 6 hours

---

*Generated as part of P1 #7 implementation*
*Last updated: 2025-10-20*
