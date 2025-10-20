"""
Testes Unitários para FacebookAdsAgent
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
import asyncio

from src.agents.facebook_agent import FacebookAdsAgent
from src.utils.config import settings


@pytest.fixture
def mock_facebook_api():
    """Mock da Facebook Marketing API"""
    with patch('src.agents.facebook_agent.FacebookAdsApi') as mock_api:
        yield mock_api


@pytest.fixture
def mock_ad_account():
    """Mock da conta de anúncios"""
    mock_account = Mock()
    mock_account.get_campaigns = Mock(return_value=[
        {
            'id': '123456',
            'name': 'Test Campaign 1',
            'status': 'ACTIVE',
            'objective': 'CONVERSIONS',
            'daily_budget': '5000',
            'lifetime_budget': None,
            'created_time': '2025-10-01T00:00:00Z',
            'updated_time': '2025-10-17T00:00:00Z'
        },
        {
            'id': '789012',
            'name': 'Test Campaign 2',
            'status': 'PAUSED',
            'objective': 'TRAFFIC',
            'daily_budget': '3000',
            'lifetime_budget': None,
            'created_time': '2025-10-01T00:00:00Z',
            'updated_time': '2025-10-17T00:00:00Z'
        }
    ])
    return mock_account


@pytest.fixture
def facebook_agent(mock_facebook_api, mock_ad_account):
    """Fixture do FacebookAdsAgent com mocks"""
    with patch.object(FacebookAdsAgent, '_init_facebook_api'):
        agent = FacebookAdsAgent()
        agent.account = mock_ad_account
        return agent


class TestFacebookAdsAgentInit:
    """Testes de inicialização do agente"""

    def test_init_loads_config(self, mock_facebook_api):
        """Verifica se configurações são carregadas corretamente"""
        with patch.object(FacebookAdsAgent, '_init_facebook_api'):
            agent = FacebookAdsAgent()

            assert agent.app_id == settings.FACEBOOK_APP_ID
            assert agent.app_secret == settings.FACEBOOK_APP_SECRET
            assert agent.access_token == settings.FACEBOOK_ACCESS_TOKEN

    def test_init_creates_components(self, mock_facebook_api):
        """Verifica criação dos componentes especializados"""
        with patch.object(FacebookAdsAgent, '_init_facebook_api'):
            agent = FacebookAdsAgent()

            assert agent.performance_analyzer is not None
            assert agent.campaign_optimizer is not None


class TestGetCampaigns:
    """Testes para método get_campaigns"""

    @pytest.mark.asyncio
    async def test_get_campaigns_active(self, facebook_agent):
        """Testa busca de campanhas ativas"""
        campaigns = await facebook_agent.get_campaigns(status_filter="ACTIVE")

        assert len(campaigns) == 2
        assert campaigns[0]['id'] == '123456'
        assert campaigns[0]['status'] == 'ACTIVE'

    @pytest.mark.asyncio
    async def test_get_campaigns_with_limit(self, facebook_agent):
        """Testa busca com limite de resultados"""
        campaigns = await facebook_agent.get_campaigns(limit=1)

        facebook_agent.account.get_campaigns.assert_called_once()
        call_params = facebook_agent.account.get_campaigns.call_args[1]['params']
        assert call_params['limit'] == 1

    @pytest.mark.asyncio
    async def test_get_campaigns_handles_exception(self, facebook_agent):
        """Testa tratamento de exceções"""
        facebook_agent.account.get_campaigns.side_effect = Exception(
            "API Error")

        with pytest.raises(Exception):
            await facebook_agent.get_campaigns()


class TestProcessNaturalLanguageQuery:
    """Testes para processamento de linguagem natural"""

    @pytest.mark.asyncio
    async def test_query_list_active_campaigns(self, facebook_agent):
        """Testa query para listar campanhas ativas"""
        response = await facebook_agent.process_natural_language_query(
            "Liste as campanhas ativas"
        )

        assert response['type'] == 'campaigns_list'
        assert 'data' in response
        assert response['query'] == "Liste as campanhas ativas"

    @pytest.mark.asyncio
    async def test_query_unknown_command(self, facebook_agent):
        """Testa query desconhecida"""
        response = await facebook_agent.process_natural_language_query(
            "Comando inexistente aleatório"
        )

        assert response['type'] == 'general_info'
        assert 'available_commands' in response['data']
