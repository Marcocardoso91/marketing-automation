"""
Gerenciador de Tokens com Renovação Automática
"""

import requests
from datetime import datetime, timedelta
from typing import Optional
from src.utils.config import settings
from src.utils.logger import setup_logger
from src.utils.exceptions import (
    InvalidTokenError,
    FacebookConnectionError
)

logger = setup_logger(__name__)


class TokenManager:
    def __init__(self):
        self.current_token = settings.FACEBOOK_ACCESS_TOKEN
        self.token_expiry: Optional[datetime] = None
        self._check_token_validity()

    def _check_token_validity(self) -> bool:
        try:
            url = "https://graph.facebook.com/debug_token"
            params = {
                'input_token': self.current_token,
                'access_token': f"{settings.FACEBOOK_APP_ID}|{settings.FACEBOOK_APP_SECRET}"
            }

            response = requests.get(url, params=params, timeout=30)
            data = response.json()

            if 'data' in data and data['data'].get('is_valid'):
                if 'expires_at' in data['data']:
                    self.token_expiry = datetime.fromtimestamp(
                        data['data']['expires_at'])
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao verificar token: {e}")
            return False

    def get_valid_token(self) -> str:
        if not self._check_token_validity():
            raise InvalidTokenError(
                message="Token validation failed - token is invalid or expired",
                details={"token_expiry": str(self.token_expiry) if self.token_expiry else None}
            )
        return self.current_token


_token_manager = None


def get_token_manager() -> TokenManager:
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager
