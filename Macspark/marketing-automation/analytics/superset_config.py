# Superset Configuration for Marketing Metrics
# Placed in: /app/pythonpath/superset_config.py

import os
from typing import Dict, Any, Optional

# Flask App Builder configuration
# Your App secret key
SECRET_KEY: str = os.getenv('SUPERSET_SECRET_KEY',
                            'CHANGE_THIS_TO_RANDOM_SECRET_KEY')

# The SQLAlchemy connection string to your database backend
SQLALCHEMY_DATABASE_URI: str = os.getenv(
    'SUPERSET_METADATA_DB_URI',
    'sqlite:////app/superset_home/superset.db'
)

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED: bool = True

# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST: list = []

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY: str = ''

# Timezone
SUPERSET_WEBSERVER_TIMEOUT: int = 60

# Default timezone
DEFAULT_TIME_ZONE: str = 'America/Sao_Paulo'

# Cache configuration
CACHE_CONFIG: Dict[str, Any] = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_'
}

# Async query configuration
RESULTS_BACKEND: Optional[str] = None

# Feature flags
FEATURE_FLAGS: Dict[str, bool] = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'DASHBOARD_VIRTUALIZATION': True,
}

# Roles
FAB_ROLES: Dict[str, list] = {
    'Public': [['can_read', 'Dashboard']],
}

# Allow embedding
ENABLE_PROXY_FIX: bool = True
HTTP_HEADERS: Dict[str, str] = {'X-Frame-Options': 'ALLOWALL'}

# Row limit for queries
ROW_LIMIT: int = 10000
SQL_MAX_ROW: int = 100000

# Language
BABEL_DEFAULT_LOCALE: str = 'pt_BR'
LANGUAGES: Dict[str, Dict[str, str]] = {
    'en': {'flag': 'us', 'name': 'English'},
    'pt': {'flag': 'br', 'name': 'Portuguese'},
    'pt_BR': {'flag': 'br', 'name': 'Portuguese (Brazil)'},
}
