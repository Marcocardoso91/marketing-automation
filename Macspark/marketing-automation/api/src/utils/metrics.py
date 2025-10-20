"""
Prometheus Metrics
Métricas customizadas da aplicação
"""
from prometheus_client import Counter, Histogram, Gauge

# Counters (eventos que só aumentam)
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

facebook_api_calls = Counter(
    'facebook_api_calls',
    'Facebook API calls',
    ['method', 'status']
)

alerts_sent = Counter(
    'alerts_sent',
    'Alerts sent',
    ['channel', 'severity']
)

suggestions_generated = Counter(
    'suggestions_generated',
    'Suggestions generated',
    ['type']
)

campaigns_analyzed = Counter(
    'campaigns_analyzed_total',
    'Total campaigns analyzed'
)

# Histograms (distribuição de valores)
request_duration = Histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    ['endpoint']
)

facebook_api_latency = Histogram(
    'facebook_api_latency_seconds',
    'Facebook API latency in seconds',
    ['method']
)

database_query_duration = Histogram(
    'database_query_duration_seconds',
    'Database query duration',
    ['table']
)

celery_task_duration = Histogram(
    'celery_task_duration_seconds',
    'Celery task duration',
    ['task_name']
)

# Gauges (valores instantâneos)
active_campaigns_count = Gauge(
    'active_campaigns',
    'Number of active campaigns'
)

daily_spend_usd = Gauge(
    'daily_spend_usd',
    'Daily spend in USD'
)

active_users_count = Gauge(
    'active_users',
    'Number of active users'
)

redis_memory_usage = Gauge(
    'redis_memory_usage_bytes',
    'Redis memory usage in bytes'
)

postgres_connections = Gauge(
    'postgres_connections_active',
    'Active PostgreSQL connections'
)
