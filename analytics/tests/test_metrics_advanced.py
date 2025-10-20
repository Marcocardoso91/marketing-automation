"""
Testes avançados para aumentar coverage
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
get_meta_ads_metrics = metrics_module.get_meta_ads_metrics
get_youtube_metrics = metrics_module.get_youtube_metrics
process_meta_ads = metrics_module.process_meta_ads
process_youtube = metrics_module.process_youtube


class TestMetaAdsAPI:
    """Testes para Meta Ads API"""

    @patch('requests.get')
    def test_get_meta_ads_error(self, mock_get, monkeypatch):
        """Testa erro na API do Meta Ads"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = get_meta_ads_metrics()

        assert result is None

    @patch('requests.get')
    def test_get_meta_ads_exception(self, mock_get):
        """Testa exceção na API do Meta Ads"""
        mock_get.side_effect = Exception("Network error")

        result = get_meta_ads_metrics()

        assert result is None

    def test_get_meta_ads_no_credentials(self, monkeypatch):
        """Testa Meta Ads sem credenciais"""
        monkeypatch.setenv("META_ACCESS_TOKEN", "")
        monkeypatch.setenv("META_AD_ACCOUNT_ID", "")

        result = get_meta_ads_metrics()

        assert result is None


class TestYouTubeAPI:
    """Testes para YouTube API"""

    @patch('requests.get')
    def test_get_youtube_error(self, mock_get, monkeypatch):
        """Testa erro na API do YouTube"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        result = get_youtube_metrics()

        assert result is None

    @patch('requests.get')
    def test_get_youtube_no_items(self, mock_get):
        """Testa YouTube sem itens na resposta"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        result = get_youtube_metrics()

        assert result is None

    @patch('requests.get')
    def test_get_youtube_exception(self, mock_get):
        """Testa exceção na API do YouTube"""
        mock_get.side_effect = Exception("Network error")

        result = get_youtube_metrics()

        assert result is None

    def test_get_youtube_no_credentials(self, monkeypatch):
        """Testa YouTube sem credenciais"""
        monkeypatch.setenv("YOUTUBE_CHANNEL_ID", "")
        monkeypatch.setenv("YOUTUBE_API_KEY", "")

        result = get_youtube_metrics()

        assert result is None


class TestDataCalculations:
    """Testes para cálculos de métricas"""

    def test_process_meta_ads_calculations(self):
        """Testa cálculos complexos de Meta Ads"""
        campaigns = [
            {
                "spend": "50.50",
                "impressions": "5000",
                "reach": "4000",
                "clicks": "75",
                "frequency": "1.25",
                "actions": [
                    {"action_type": "follow", "value": "25"},
                    {"action_type": "onsite_conversion.post_save", "value": "10"},
                ],
            }
        ]

        result = process_meta_ads(campaigns)

        assert result is not None
        assert result["spend"] == 50.50
        assert result["new_followers"] == 35  # 25 + 10
        assert result["cost_per_follower"] == pytest.approx(1.44, rel=0.01)

    def test_process_meta_ads_no_actions(self):
        """Testa Meta Ads sem ações"""
        campaigns = [
            {
                "spend": "100",
                "impressions": "10000",
                "reach": "8000",
                "clicks": "150",
                "frequency": "1.25",
                "actions": [],
            }
        ]

        result = process_meta_ads(campaigns)

        assert result is not None
        assert result["new_followers"] == 0
        assert result["cost_per_follower"] == 0

    def test_process_youtube_calculations(self):
        """Testa cálculos do YouTube"""
        stats = {"viewCount": "200000", "subscriberCount": "10000"}

        result = process_youtube(stats)

        assert result is not None
        assert result["views"] > 0
        assert result["subscribers_gained"] > 0
        assert "notes" in result
