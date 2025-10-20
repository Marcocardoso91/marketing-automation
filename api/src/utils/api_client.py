"""
Compat layer para o cliente Facebook compartilhado.
"""

from marketing_shared.utils import (
    FacebookAPIClient,
    RateLimitException,
    get_facebook_api_client,
)

# Mantém compatibilidade com importações antigas
get_api_client = get_facebook_api_client
