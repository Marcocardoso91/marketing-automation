"""
Testes de Integração - APIs REST
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from main import app
from src.utils.auth import get_current_user

client = TestClient(app)


@pytest.fixture(autouse=True)
def _override_auth_dependency():
    """Garantir que endpoints autenticados aceitem requisições de teste."""
    app.dependency_overrides[get_current_user] = lambda: {"sub": "test-user@example.com"}
    yield
    app.dependency_overrides.pop(get_current_user, None)

class TestCampaignsAPI:
    """Testes da API de Campanhas"""

    def test_get_campaigns_endpoint(self):
        """Testa endpoint de listagem de campanhas"""
        with patch('src.api.campaigns.FacebookAdsAgent') as mock_agent:
            mock_instance = mock_agent.return_value
            mock_instance.get_campaigns = AsyncMock(return_value=[
                {
                    'id': '123',
                    'name': 'Test Campaign',
                    'status': 'ACTIVE',
                    'objective': 'CONVERSIONS',
                    'daily_budget': '5000',
                    'lifetime_budget': None,
                    'created_time': '2025-10-01T00:00:00Z',
                    'updated_time': '2025-10-17T00:00:00Z'
                }
            ])

            response = client.get("/api/v1/campaigns?status=ACTIVE")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]['id'] == '123'

    def test_get_campaign_insights_endpoint(self):
        """Testa endpoint de insights de campanha"""
        with patch('src.api.campaigns.FacebookAdsAgent') as mock_agent:
            mock_instance = mock_agent.return_value
            mock_instance.get_campaign_insights = AsyncMock(return_value={
                'campaign_id': '123',
                'impressions': 10000,
                'clicks': 500,
                'spend': 1000.0,
                'ctr': 5.0,
                'cpc': 2.0,
                'cpm': 100.0,
                'reach': 8000,
                'frequency': 1.25,
                'cpa': 40.0,
                'roas': 3.5,
                'date_range': 'last_7d'
            })

            response = client.get("/api/v1/campaigns/123/insights")

            assert response.status_code == 200
            data = response.json()
            assert data['campaign_id'] == '123'
            assert data['ctr'] == 5.0

class TestAnalyticsAPI:
    """Testes da API de Analytics"""

    def test_dashboard_data_endpoint(self):
        """Testa endpoint de dados do dashboard"""
        with patch('src.api.analytics.FacebookAdsAgent') as mock_agent:
            mock_instance = mock_agent.return_value
            mock_instance.get_campaigns = AsyncMock(return_value=[
                {'id': '1', 'name': 'Campaign 1', 'status': 'ACTIVE'},
                {'id': '2', 'name': 'Campaign 2', 'status': 'ACTIVE'}
            ])
            mock_instance.get_campaign_insights = AsyncMock(return_value={
                'spend': 500.0,
                'impressions': 10000,
                'clicks': 200,
                'ctr': 2.0,
                'cpc': 2.5
            })

            response = client.get("/api/v1/analytics/dashboard")

            assert response.status_code == 200
            data = response.json()
            assert 'summary' in data
            assert 'top_campaigns' in data

class TestAutomationAPI:
    """Testes da API de Automação"""

    def test_pause_underperforming_endpoint(self):
        """Testa endpoint de pausa automática"""
        with patch('src.api.automation.FacebookAdsAgent') as mock_agent:
            mock_instance = mock_agent.return_value
            mock_instance.get_campaigns = AsyncMock(return_value=[
                {'id': '123', 'name': 'Low CTR Campaign', 'status': 'ACTIVE'}
            ])
            mock_instance.get_campaign_insights = AsyncMock(return_value={
                'ctr': 0.5,
                'cpa': 100.0,
                'spend': 200.0
            })

            response = client.post(
                "/api/v1/automation/pause-underperforming",
                params={'ctr_threshold': 0.8, 'cpa_threshold': 50.0}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
        assert 'CTR baixo' in data[0]['reason']

class TestHealthEndpoints:
    """Testes de endpoints de saúde"""

    def test_health_check(self):
        """Testa health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'

    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = client.get("/")

        assert response.status_code == 200
        assert "Facebook Ads AI Agent" in response.text
