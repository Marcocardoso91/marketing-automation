"""
Wrapper para reutilizar os testes de integração definidos em `backend/tests`.
Evita duplicar lógica entre diretórios mantendo o runner legado compatível.
"""
import pytest

from backend.tests.integration.test_api_integration import (  # noqa: F401,F403
    TestCampaignsAPI,
    TestAnalyticsAPI,
    TestAutomationAPI,
    TestHealthEndpoints,
)

# Exporta testes adicionais (schema validation) do pacote compartilhado
from backend.tests.integration.test_api_integration import *  # noqa: F401,F403,E402


class TestSchemaValidation:
    """Testes de validação de schemas Pydantic (apoiam CI antigo)"""

    def test_campaign_metric_schema_valid(self):
        """Testa criação de schema válido"""
        from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema
        from datetime import date as Date

        metric = CampaignMetricSchema(
            campaign_id="123",
            campaign_name="Test Campaign",
            date=Date(2025, 10, 18),
            impressions=1000,
            clicks=50,
            spend=100.0,
            reach=800,
            frequency=1.25,
            ctr=5.0,
            cpc=2.0,
            conversions=10
        )

        assert metric.campaign_id == "123"
        assert metric.impressions == 1000

    def test_campaign_metric_schema_validates_negatives(self):
        """Testa que valores negativos são rejeitados"""
        from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema
        from pydantic import ValidationError
        from datetime import date as Date

        with pytest.raises(ValidationError):
            CampaignMetricSchema(
                campaign_id="123",
                campaign_name="Test",
                date=Date(2025, 10, 18),
                impressions=-100,  # Inválido
                clicks=50,
                spend=100.0,
                reach=800,
                frequency=1.25,
                ctr=5.0,
                cpc=2.0,
                conversions=10
            )
