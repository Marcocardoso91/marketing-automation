"""
Testes para o script validate-env.py
"""
import importlib.util
import pytest
import os
from unittest.mock import patch
import sys

# Adicionar o diretório scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


# Import validate_env module
spec = importlib.util.spec_from_file_location(
    "validate_env", "scripts/validate-env.py")
validate_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_module)

# Import functions and constants
validate_env = validate_module.validate_env
show_env_status = validate_module.show_env_status
REQUIRED_VARS = validate_module.REQUIRED_VARS
OPTIONAL_VARS = validate_module.OPTIONAL_VARS


class TestValidateEnv:
    """Testes para validação de variáveis de ambiente"""

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'test-url',
        'SUPABASE_SERVICE_KEY': 'test-key',
        'META_ACCESS_TOKEN': 'test-token',
        'META_AD_ACCOUNT_ID': 'test-account'
    })
    def test_validate_env_all_required_present(self):
        """Testa validação quando todas as variáveis obrigatórias estão presentes"""
        result = validate_env()
        assert result is True

    @patch.dict(os.environ, {}, clear=True)
    def test_validate_env_missing_required(self):
        """Testa validação quando variáveis obrigatórias estão faltando"""
        result = validate_env()
        assert result is False

    def test_required_vars_list(self):
        """Testa se a lista de variáveis obrigatórias está correta"""
        expected = [
            'SUPABASE_URL',
            'SUPABASE_SERVICE_KEY',
            'META_ACCESS_TOKEN',
            'META_AD_ACCOUNT_ID'
        ]
        assert REQUIRED_VARS == expected

    def test_optional_vars_list(self):
        """Testa se a lista de variáveis opcionais está correta"""
        expected = [
            'GA4_PROPERTY_ID',
            'GOOGLE_ADS_CUSTOMER_ID',
            'YOUTUBE_CHANNEL_ID',
            'YOUTUBE_API_KEY',
            'OPENAI_API_KEY',
            'SLACK_WEBHOOK_URL',
            'NOTION_TOKEN',
            'NOTION_DATABASE_ID'
        ]
        assert OPTIONAL_VARS == expected

    @patch.dict(os.environ, {
        'SUPABASE_URL': 'test-url',
        'SUPABASE_SERVICE_KEY': 'test-key',
        'META_ACCESS_TOKEN': 'test-token',
        'META_AD_ACCOUNT_ID': 'test-account',
        'GA4_PROPERTY_ID': 'test-ga4',
        'OPENAI_API_KEY': 'test-openai'
    })
    def test_validate_env_mixed_optional(self):
        """Testa validação com algumas variáveis opcionais configuradas"""
        result = validate_env()
        assert result is True
