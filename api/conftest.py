"""
Configurações e fixtures compartilhadas para testes
"""

import pytest
import asyncio
from typing import Generator
from unittest.mock import Mock, patch

from src.utils.config import settings

@pytest.fixture(scope="session")
def event_loop():
    """Cria um event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_settings():
    """Mock das configurações da aplicação"""
    with patch.object(settings, 'FACEBOOK_APP_ID', 'test_app_id'):
        with patch.object(settings, 'FACEBOOK_APP_SECRET', 'test_app_secret'):
            with patch.object(settings, 'FACEBOOK_ACCESS_TOKEN', 'test_token'):
                with patch.object(settings, 'FACEBOOK_AD_ACCOUNT_ID', 'test_account'):
                    yield settings

@pytest.fixture
def sample_campaign_data():
    """Dados de exemplo de uma campanha"""
    return {
        'id': '123456789',
        'name': 'Test Campaign',
        'status': 'ACTIVE',
        'objective': 'CONVERSIONS',
        'daily_budget': '5000',
        'lifetime_budget': None,
        'created_time': '2025-10-01T00:00:00+0000',
        'updated_time': '2025-10-17T00:00:00+0000'
    }

@pytest.fixture
def sample_insights_data():
    """Dados de exemplo de insights de campanha"""
    return {
        'campaign_id': '123456789',
        'impressions': 10000,
        'clicks': 500,
        'spend': 1250.50,
        'ctr': 5.0,
        'cpc': 2.50,
        'cpm': 125.05,
        'reach': 8000,
        'frequency': 1.25,
        'purchases': 25,
        'cpa': 50.02,
        'roas': 3.5,
        'date_range': 'last_7d'
    }

@pytest.fixture
def mock_facebook_api_client():
    """Mock do cliente da Facebook API"""
    with patch('facebook_business.api.FacebookAdsApi') as mock_api:
        mock_api.init = Mock()
        yield mock_api
