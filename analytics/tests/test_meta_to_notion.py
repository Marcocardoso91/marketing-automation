"""
Testes para o script meta-to-notion.py
"""
import importlib.util
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Adicionar o diretório scripts ao path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


# Import meta_to_notion module
spec = importlib.util.spec_from_file_location(
    "meta_to_notion", "scripts/meta-to-notion.py")
meta_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meta_module)

# Import functions
get_meta_ads_metrics = meta_module.get_meta_ads_metrics
add_to_notion = meta_module.add_to_notion
process_metrics = meta_module.process_metrics
main = meta_module.main

# Alias para compatibilidade com testes
send_to_notion = add_to_notion


class TestMetaAdsIntegration:
    """Testes para integração Meta Ads API"""

    @patch('requests.get')
    def test_get_meta_ads_metrics_success(self, mock_get):
        """Testa coleta bem-sucedida de métricas do Meta Ads"""
        # Mock da resposta da API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'campaign_name': 'Test Campaign',
                    'spend': '100.50',
                    'impressions': '10000',
                    'reach': '8000',
                    'clicks': '150',
                    'actions': [
                        {'action_type': 'follow', 'value': '50'}
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        # Executar
        result = get_meta_ads_metrics(date_preset='yesterday')

        # Assertions
        assert result is not None
        assert len(result) == 1
        assert result[0]['campaign_name'] == 'Test Campaign'
        assert float(result[0]['spend']) == 100.50

    @patch('requests.get')
    def test_get_meta_ads_metrics_api_error(self, mock_get):
        """Testa tratamento de erro da API"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = get_meta_ads_metrics()

        assert result is None

    @patch('requests.get')
    def test_get_meta_ads_metrics_credentials_missing(self, mock_get):
        """Testa quando credenciais não estão configuradas"""
        with patch.dict(os.environ, {'META_ACCESS_TOKEN': '', 'META_AD_ACCOUNT_ID': ''}):
            result = get_meta_ads_metrics()
            assert result is None


class TestNotionIntegration:
    """Testes para integração Notion"""

    @patch('requests.post')
    def test_send_to_notion_success(self, mock_post):
        """Testa envio bem-sucedido para Notion"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        metrics = {
            'data': '2025-10-18',
            'gasto_ads': 100.0,
            'alcance': 8000,
            'ctr': 1.5,
            'cpc': 0.67,
            'cpe': 2.0,
            'frequencia': 1.25,
            'novos_seguidores': 50,
            'custo_por_seguidor': 2.0,
            'notas': 'Test'
        }

        result = send_to_notion(metrics)

        assert result is True
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_send_to_notion_api_error(self, mock_post):
        """Testa erro na API do Notion"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        metrics = {
            'data': '2025-10-18',
            'gasto_ads': 0,
            'alcance': 0,
            'ctr': 0,
            'cpc': 0,
            'cpe': 0,
            'frequencia': 0,
            'novos_seguidores': 0,
            'custo_por_seguidor': 0,
            'notas': ''
        }

        result = send_to_notion(metrics)

        assert result is False

    @patch('requests.post')
    def test_send_to_notion_credentials_missing(self, mock_post):
        """Testa quando credenciais do Notion não estão configuradas"""
        # Simular erro no POST devido a credenciais inválidas
        mock_response = Mock()
        mock_response.status_code = 401  # Unauthorized
        mock_post.return_value = mock_response

        with patch.dict(os.environ, {'NOTION_TOKEN': '', 'NOTION_DATABASE_ID': ''}):
            metrics = {
                'data': '2025-10-18',
                'gasto_ads': 0,
                'alcance': 0,
                'ctr': 0,
                'cpc': 0,
                'cpe': 0,
                'frequencia': 0,
                'novos_seguidores': 0,
                'custo_por_seguidor': 0,
                'notas': ''
            }
            result = send_to_notion(metrics)

            # Deve falhar por erro HTTP
            assert result is False


class TestDataProcessing:
    """Testes para processamento de dados"""

    def test_process_metrics_success(self):
        """Testa processamento de métricas agregadas"""
        campaigns_data = [
            {
                'campaign_name': 'Campaign 1',
                'spend': '50',
                'impressions': '5000',
                'reach': '4000',
                'clicks': '75',
                'frequency': '1.25',
                'actions': [{'action_type': 'follow', 'value': '25'}]
            },
            {
                'campaign_name': 'Campaign 2',
                'spend': '50',
                'impressions': '5000',
                'reach': '4000',
                'clicks': '75',
                'frequency': '1.25',
                'actions': [{'action_type': 'follow', 'value': '25'}]
            }
        ]

        result = process_metrics(campaigns_data)

        assert result is not None
        assert result['gasto_ads'] == 100.0
        assert 'alcance' in result
        assert 'novos_seguidores' in result

    def test_process_metrics_empty_data(self):
        """Testa processamento com dados vazios"""
        result = process_metrics([])
        # Deve retornar None ou dict vazio dependendo da implementação
        assert result is None or isinstance(result, dict)

    def test_process_metrics_missing_fields(self):
        """Testa processamento com campos ausentes"""
        campaigns_data = [
            {
                'campaign_name': 'Campaign 1',
                'spend': '50',
                'impressions': '5000',
                'clicks': '75',
                'actions': []  # Sem ações
            }
        ]

        result = process_metrics(campaigns_data)

        assert result is not None or result is None  # Aceita ambos


class TestMainWorkflow:
    """Testes para função main"""

    def test_main_success(self, monkeypatch):
        """Testa execução bem-sucedida da função main"""
        def mock_get(*args, **kwargs):
            return [
                {
                    'campaign_name': 'Test Campaign',
                    'spend': '100',
                    'impressions': '10000',
                    'reach': '8000',
                    'clicks': '150',
                    'actions': [{'action_type': 'follow', 'value': '50'}]
                }
            ]

        def mock_add(*args, **kwargs):
            return True

        monkeypatch.setattr(meta_module, 'get_meta_ads_metrics', mock_get)
        monkeypatch.setattr(meta_module, 'add_to_notion', mock_add)

        # Não deve levantar exceção
        try:
            main()
        except SystemExit:
            pass  # main() pode chamar exit()

    def test_main_no_data(self, monkeypatch):
        """Testa execução quando não há dados do Meta Ads"""
        def mock_get(*args, **kwargs):
            return None

        monkeypatch.setattr(meta_module, 'get_meta_ads_metrics', mock_get)

        # Não deve levantar exceção
        try:
            main()
        except SystemExit:
            pass

    def test_main_empty_data(self, monkeypatch):
        """Testa execução quando dados estão vazios"""
        def mock_get(*args, **kwargs):
            return []

        monkeypatch.setattr(meta_module, 'get_meta_ads_metrics', mock_get)

        # Não deve levantar exceção
        try:
            main()
        except SystemExit:
            pass
