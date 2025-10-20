"""
Configuration file for pytest tests
"""
import pytest
import os
from unittest.mock import Mock


@pytest.fixture(scope='session', autouse=True)
def setup_test_env():
    """Configura variáveis de ambiente para testes"""
    os.environ['SUPABASE_URL'] = 'http://test.supabase.co'
    os.environ['SUPABASE_SERVICE_KEY'] = 'test-key'
    os.environ['META_ACCESS_TOKEN'] = 'test-token'
    os.environ['META_AD_ACCOUNT_ID'] = 'act_123456'
    os.environ['YOUTUBE_API_KEY'] = 'test-youtube-key'
    os.environ['YOUTUBE_CHANNEL_ID'] = 'UC123456'
    os.environ['OPENAI_API_KEY'] = 'sk-test-key'
    os.environ['SLACK_WEBHOOK_URL'] = 'https://hooks.slack.com/test'
    os.environ['NOTION_TOKEN'] = 'test-notion-token'
    os.environ['NOTION_DATABASE_ID'] = 'test-db-id'

    yield

    # Cleanup (opcional)
    pass


@pytest.fixture
def sample_meta_ads_data():
    """Fixture com dados de exemplo do Meta Ads"""
    return [
        {
            'campaign_name': 'Campaign 1',
            'spend': '50',
            'impressions': '5000',
            'clicks': '75',
            'actions': [{'action_type': 'follow', 'value': '25'}]
        }
    ]


@pytest.fixture
def mock_supabase_client():
    """Fixture com cliente Supabase mockado"""
    client = Mock()
    client.table.return_value.upsert.return_value.execute.return_value = Mock()
    return client


@pytest.fixture
def mock_openai_client():
    """Fixture com cliente OpenAI mockado"""
    client = Mock()
    response = Mock()
    response.choices = [Mock(message=Mock(content='Test insight'))]
    client.chat.completions.create.return_value = response
    return client


@pytest.fixture
def sample_youtube_data():
    """Fixture com dados de exemplo do YouTube"""
    return {
        'viewCount': '100000',
        'subscriberCount': '5000'
    }


@pytest.fixture
def sample_consolidated_data():
    """Fixture com dados consolidados"""
    return {
        'data': '2025-10-18',
        'total_spend': 100.0,
        'total_followers': 50,
        'avg_cost_per_follower': 2.0,
        'avg_ctr': 1.5,
        'by_source': {
            'meta_ads': {'spend': 100.0, 'followers': 50, 'ctr': 1.5}
        }
    }
