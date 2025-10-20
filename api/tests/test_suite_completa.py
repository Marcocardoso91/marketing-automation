"""
Test Suite Completa - Facebook Ads AI Agent
Testa todas as funcionalidades implementadas
"""
import pytest
import asyncio
import os
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

HAS_ENV_FILE = os.path.exists('.env')
skip_if_no_env = pytest.mark.skipif(not HAS_ENV_FILE, reason=".env file not available")
RUN_N8N_E2E = os.getenv("RUN_N8N_E2E") == "1"
skip_n8n_e2e = pytest.mark.skipif(
    not RUN_N8N_E2E or not (os.getenv('N8N_API_URL') and os.getenv('N8N_API_KEY')),
    reason="Set RUN_N8N_E2E=1 e configure N8N_API_URL/N8N_API_KEY para executar testes reais"
)


# ============================================================================
# TEST 1: CONFIGURAÇÃO E AMBIENTE
# ============================================================================

@skip_if_no_env
class TestEnvironmentSetup:
    """Testa se o ambiente está configurado corretamente"""

    def test_env_file_exists(self):
        """Verifica se .env existe"""
        assert os.path.exists('.env'), ".env file not found"

    def test_n8n_credentials_configured(self):
        """Verifica se credenciais n8n estão configuradas"""
        from dotenv import load_dotenv
        load_dotenv()

        if not os.getenv('N8N_API_URL') or not os.getenv('N8N_API_KEY') or not os.getenv('N8N_WEBHOOK_URL'):
            pytest.skip("n8n credentials not configured")

    def test_project_structure(self):
        """Verifica estrutura de diretórios"""
        required_dirs = [
            'src', 'src/agents', 'src/api', 'src/analytics',
            'src/automation', 'src/integrations', 'src/models',
            'src/tasks', 'src/utils', 'tests', 'docs', 'config'
        ]

        for directory in required_dirs:
            assert os.path.exists(
                directory), f"Directory {directory} not found"


# ============================================================================
# TEST 2: MODELS (SQLAlchemy)
# ============================================================================

class TestModels:
    """Testa modelos de dados"""

    def test_campaign_model_import(self):
        """Testa import do modelo Campaign"""
        from src.models.campaign import Campaign
        assert Campaign is not None

    def test_insight_model_import(self):
        """Testa import do modelo Insight"""
        from src.models.insight import Insight
        assert Insight is not None

    def test_user_model_import(self):
        """Testa import do modelo User"""
        from src.models.user import User
        assert User is not None

    def test_conversation_model_import(self):
        """Testa import do modelo ConversationMemory"""
        from src.models.conversation import ConversationMemory
        assert ConversationMemory is not None


# ============================================================================
# TEST 3: SCHEMAS (Pydantic)
# ============================================================================

class TestSchemas:
    """Testa schemas Pydantic"""

    def test_campaign_schema(self):
        """Testa schema de Campaign"""
        from src.schemas.campaign_schemas import CampaignResponse
        from datetime import datetime

        campaign_data = {
            "id": "123",
            "name": "Test Campaign",
            "status": "ACTIVE",
            "daily_budget": 100.0,
            "synced_at": datetime.now()
        }

        campaign = CampaignResponse(**campaign_data)
        assert campaign.id == "123"
        assert campaign.name == "Test Campaign"

    def test_insight_schema(self):
        """Testa schema de Insight"""
        from src.schemas.insight_schemas import InsightResponse
        from datetime import datetime, date

        insight_data = {
            "id": "insight-1",
            "campaign_id": "123",
            "date": date.today(),
            "impressions": 1000,
            "clicks": 50,
            "spend": 25.50,
            "ctr": 5.0,
            "cpc": 0.51,
            "collected_at": datetime.now()
        }

        insight = InsightResponse(**insight_data)
        assert insight.impressions == 1000
        assert insight.ctr == 5.0


# ============================================================================
# TEST 4: INTEGRAÇÕES
# ============================================================================

class TestIntegrations:
    """Testa integrações externas"""

    def test_n8n_client_import(self):
        """Testa import do N8nClient"""
        from src.integrations.n8n_client import N8nClient
        assert N8nClient is not None

    def test_n8n_manager_import(self):
        """Testa import do N8nWorkflowManager"""
        from src.integrations.n8n_manager import N8nWorkflowManager
        assert N8nWorkflowManager is not None

    def test_notion_client_import(self):
        """Testa import do NotionClient"""
        from src.integrations.notion_client import NotionClient
        assert NotionClient is not None

    @pytest.mark.asyncio
    async def test_n8n_manager_initialization(self):
        """Testa inicialização do N8nManager"""
        from src.integrations.n8n_manager import N8nWorkflowManager

        manager = N8nWorkflowManager()
        assert manager.api_url is not None
        assert "fluxos.macspark.dev" in manager.api_url

    @pytest.mark.asyncio
    async def test_notion_client_initialization(self):
        """Testa inicialização do NotionClient"""
        from src.integrations.notion_client import NotionClient

        client = NotionClient(database_id="test-db")
        assert client.database_id == "test-db"


# ============================================================================
# TEST 5: AGENTS E ANALYTICS
# ============================================================================

class TestAgentsAndAnalytics:
    """Testa agentes e análise"""

    def test_facebook_agent_import(self):
        """Testa import do FacebookAdsAgent"""
        from src.agents.facebook_agent import FacebookAdsAgent
        assert FacebookAdsAgent is not None

    def test_performance_analyzer_import(self):
        """Testa import do PerformanceAnalyzer"""
        from src.analytics.performance_analyzer import PerformanceAnalyzer
        assert PerformanceAnalyzer is not None

    def test_campaign_optimizer_import(self):
        """Testa import do CampaignOptimizer"""
        from src.automation.campaign_optimizer import CampaignOptimizer
        assert CampaignOptimizer is not None

    def test_performance_analyzer_score_calculation(self):
        """Testa cálculo de score"""
        from src.analytics.performance_analyzer import PerformanceAnalyzer

        analyzer = PerformanceAnalyzer()

        # Mock insights
        insights = {
            'ctr': 3.5,
            'cpc': 0.75,
            'cpa': 25.0,
            'frequency': 2.0,
            'roas': 4.0
        }

        score = analyzer.calculate_score(insights)
        assert 0 <= score <= 100
        assert score > 50  # Good metrics should give good score


# ============================================================================
# TEST 6: API ENDPOINTS
# ============================================================================

class TestAPIEndpoints:
    """Testa endpoints FastAPI"""

    def test_main_app_import(self):
        """Testa import do app principal"""
        from main import app
        assert app is not None

    def test_campaigns_router_import(self):
        """Testa import do campaigns router"""
        from src.api.campaigns import router
        assert router is not None

    def test_analytics_router_import(self):
        """Testa import do analytics router"""
        from src.api.analytics import router
        assert router is not None

    def test_notion_router_import(self):
        """Testa import do notion router"""
        from src.api.notion import router
        assert router is not None

    def test_n8n_admin_router_import(self):
        """Testa import do n8n admin router"""
        from src.api.n8n_admin import router
        assert router is not None


# ============================================================================
# TEST 7: CELERY TASKS
# ============================================================================

class TestCeleryTasks:
    """Testa Celery tasks"""

    def test_celery_app_import(self):
        """Testa import do Celery app"""
        from src.tasks.celery_app import celery_app
        assert celery_app is not None

    def test_collectors_import(self):
        """Testa import dos collectors"""
        from src.tasks.collectors import collect_facebook_metrics
        assert collect_facebook_metrics is not None

    def test_processors_import(self):
        """Testa import dos processors"""
        from src.tasks.processors import analyze_performance
        assert analyze_performance is not None

    def test_notifiers_import(self):
        """Testa import dos notifiers"""
        from src.tasks.notifiers import send_alert
        assert send_alert is not None


# ============================================================================
# TEST 8: UTILS
# ============================================================================

class TestUtils:
    """Testa utilitários"""

    def test_config_import(self):
        """Testa import das configurações"""
        from src.utils.config import settings
        assert settings is not None

    def test_logger_import(self):
        """Testa import do logger"""
        from src.utils.logger import setup_logger

        logger = setup_logger("test")
        assert logger is not None

    def test_metrics_import(self):
        """Testa import das métricas"""
        from src.utils.metrics import (
            facebook_api_calls,
            active_campaigns_count
        )
        assert facebook_api_calls is not None
        assert active_campaigns_count is not None


# ============================================================================
# TEST 9: INTEGRAÇÃO N8N (Real)
# ============================================================================

@skip_n8n_e2e
class TestN8nIntegrationReal:
    """Testa integração real com n8n Macspark"""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_n8n_api_connection(self):
        """Testa conexão real com API n8n"""
        import httpx
        from dotenv import load_dotenv
        load_dotenv()

        api_url = os.getenv("N8N_API_URL")
        api_key = os.getenv("N8N_API_KEY")

        if not api_key:
            pytest.skip("N8N_API_KEY not configured")

        headers = {
            "X-N8N-API-KEY": api_key,
            "Accept": "application/json"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{api_url}/workflows", headers=headers)

            assert response.status_code == 200
            data = response.json()
            assert 'data' in data
            assert len(data['data']) >= 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_n8n_workflow_discovery(self):
        """Testa descoberta de workflows"""
        from src.integrations.n8n_manager import get_n8n_manager

        manager = get_n8n_manager()
        workflows = await manager.list_workflows()

        # Should return list (empty or with workflows)
        assert isinstance(workflows, list)


# ============================================================================
# TEST 10: DOCUMENTAÇÃO
# ============================================================================

class TestDocumentation:
    """Testa se documentação existe"""

    def test_readme_exists(self):
        """Verifica se README existe"""
        assert os.path.exists('README.md')

    def test_audit_docs_exist(self):
        """Verifica se docs de auditoria existem"""
        docs = [
            'docs/RUNBOOK.md',
            'docs/DEPLOYMENT.md',
            'docs/INTEGRACAO-NOTION-N8N.md',
            'docs/SETUP-N8N-MACSPARK.md'
        ]

        for doc in docs:
            assert os.path.exists(doc), f"{doc} not found"

    def test_integration_docs_exist(self):
        """Verifica docs de integração"""
        assert os.path.exists('INTEGRACAO-MCP-COMPLETA.md')
        assert os.path.exists('INTEGRACAO-ATIVA-N8N-MACSPARK.md')
        assert os.path.exists('00-LEIA-PRIMEIRO-INTEGRACAO-N8N.md')


# ============================================================================
# TEST 11: DOCKER E DEPLOY
# ============================================================================

class TestDockerAndDeploy:
    """Testa configurações Docker"""

    def test_dockerfile_exists(self):
        """Verifica se Dockerfile existe"""
        assert os.path.exists('Dockerfile')

    def test_docker_compose_exists(self):
        """Verifica se docker-compose existe"""
        assert os.path.exists('docker-compose.yml')

    def test_docker_compose_prod_exists(self):
        """Verifica se docker-compose.prod existe"""
        assert os.path.exists('docker-compose.prod.yml')

    def test_requirements_exists(self):
        """Verifica se requirements.txt existe"""
        assert os.path.exists('requirements.txt')

    def test_alembic_config_exists(self):
        """Verifica se alembic.ini existe"""
        assert os.path.exists('alembic.ini')


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

@pytest.fixture
def sample_campaign():
    """Fixture com campanha de exemplo"""
    return {
        'id': '123456',
        'name': 'Test Campaign',
        'status': 'ACTIVE',
        'daily_budget': 100.0,
        'insights': {
            'impressions': 10000,
            'clicks': 500,
            'spend': 50.0,
            'ctr': 5.0,
            'cpc': 0.10,
            'cpm': 5.0,
            'cpa': 10.0,
            'frequency': 2.0,
            'reach': 5000,
            'purchases': 5,
            'revenue': 500.0,
            'roas': 10.0
        }
    }


@pytest.fixture
def sample_insights():
    """Fixture com insights de exemplo"""
    return {
        'impressions': 10000,
        'clicks': 500,
        'spend': 50.0,
        'ctr': 5.0,
        'cpc': 0.10,
        'cpm': 5.0,
        'cpa': 10.0,
        'frequency': 2.0,
        'reach': 5000
    }


# ============================================================================
# SUMMARY
# ============================================================================

def test_summary():
    """
    Test Summary - Facebook Ads AI Agent

    Total Test Categories: 11
    - Environment Setup
    - Models (SQLAlchemy)
    - Schemas (Pydantic)
    - Integrations (n8n, Notion)
    - Agents & Analytics
    - API Endpoints
    - Celery Tasks
    - Utils
    - N8N Integration (Real)
    - Documentation
    - Docker & Deploy
    """
    assert True  # Summary test always passes
