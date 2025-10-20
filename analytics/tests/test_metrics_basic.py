"""
Testes básicos para funções de métricas
"""
import pytest
import os
from unittest.mock import Mock, patch
import sys
import importlib.util

# Adicionar o diretório scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Import metrics_to_supabase module
spec = importlib.util.spec_from_file_location(
    "metrics_to_supabase", "scripts/metrics-to-supabase.py"
)
metrics_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics_module)

# Import functions
process_meta_ads = metrics_module.process_meta_ads
process_youtube = metrics_module.process_youtube
get_google_analytics_metrics = metrics_module.get_google_analytics_metrics
get_google_ads_metrics = metrics_module.get_google_ads_metrics
save_to_supabase = metrics_module.save_to_supabase
consolidate_metrics = metrics_module.consolidate_metrics
generate_insights_openai = metrics_module.generate_insights_openai
send_slack_notification = metrics_module.send_slack_notification


class TestDataProcessing:
    """Testes para processamento de dados"""

    def test_process_meta_ads_empty(self):
        """Testa processamento de Meta Ads com dados vazios"""
        result = process_meta_ads([])
        assert result is None

    def test_process_meta_ads_success(self):
        """Testa processamento de Meta Ads com dados válidos"""
        campaigns = [
            {
                "spend": "100",
                "impressions": "10000",
                "reach": "8000",
                "clicks": "150",
                "frequency": "1.25",
                "actions": [{"action_type": "follow", "value": "50"}],
            }
        ]

        result = process_meta_ads(campaigns)

        assert result is not None
        assert result["spend"] == 100.0
        assert result["impressions"] == 10000
        assert result["new_followers"] == 50
        assert result["cost_per_follower"] == 2.0

    def test_process_youtube_none(self):
        """Testa processamento de YouTube com None"""
        result = process_youtube(None)
        assert result is None

    def test_process_youtube_success(self):
        """Testa processamento de YouTube com dados válidos"""
        stats = {"viewCount": "100000", "subscriberCount": "5000"}

        result = process_youtube(stats)

        assert result is not None
        assert result["source"] == "youtube"
        assert result["spend"] == 0


class TestAPIPlaceholders:
    """Testes para funções placeholder"""

    def test_google_analytics_placeholder(self):
        """Testa função placeholder do Google Analytics"""
        result = get_google_analytics_metrics()
        assert result is None

    def test_google_ads_placeholder(self):
        """Testa função placeholder do Google Ads"""
        result = get_google_ads_metrics()
        assert result is None


class TestSupabaseNoClient:
    """Testes para Supabase sem cliente configurado"""

    def test_save_to_supabase_no_client(self, monkeypatch):
        """Testa save_to_supabase sem cliente"""
        monkeypatch.setattr(metrics_module, "supabase", None)

        metrics = {"data": "2025-10-18", "source": "test"}

        result = save_to_supabase(metrics)

        assert result is False

    def test_consolidate_metrics_no_client(self, monkeypatch):
        """Testa consolidate_metrics sem cliente"""
        monkeypatch.setattr(metrics_module, "supabase", None)

        result = consolidate_metrics("2025-10-18")

        assert result is None


class TestOpenAINoClient:
    """Testes para OpenAI sem cliente configurado"""

    def test_generate_insights_no_client(self, monkeypatch):
        """Testa generate_insights sem cliente OpenAI"""
        monkeypatch.setattr(metrics_module, "openai_client", None)

        consolidated = {
            "data": "2025-10-18",
            "total_spend": 0,
            "total_reach": 0,
            "total_followers": 0,
            "avg_cost_per_follower": 0,
            "avg_ctr": 0,
            "by_source": {},
        }

        result = generate_insights_openai(consolidated)

        assert "OpenAI não configurado" in result or "Erro" in result


class TestSlackNoWebhook:
    """Testes para Slack sem webhook configurado"""

    def test_send_slack_no_webhook(self, monkeypatch):
        """Testa send_slack sem webhook configurado"""
        monkeypatch.setenv("SLACK_WEBHOOK_URL", "")

        consolidated = {
            "data": "2025-10-18",
            "total_spend": 100,
            "total_reach": 1000,
            "total_followers": 50,
            "avg_cost_per_follower": 2.0,
        }

        result = send_slack_notification(consolidated, "Test insight")

        assert result is False
