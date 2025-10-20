"""
Celery Tasks - Data Collectors
"""
from src.tasks.celery_app import celery_app
from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5) - shorter TTL for background tasks
from src.utils.agent_cache import get_cached_agent_provider
from src.utils.metrics import facebook_api_calls, campaigns_analyzed
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@celery_app.task(name='src.tasks.collectors.collect_facebook_metrics')
def collect_facebook_metrics():
    """
    Collect metrics from Facebook Ads
    Runs every 30 minutes
    """
    import asyncio

    async def _collect():
        try:
            # Use shorter cache TTL for background tasks (30min)
            provider = get_cached_agent_provider(cache_ttl=1800)
            agent = provider.get_agent()
        except Exception as exc:
            logger.error(f"Failed to initialize Facebook agent: {exc}")
            facebook_api_calls.labels(method='INIT', status='error').inc()
            return 0

        try:
            campaigns = await agent.get_campaigns(status_filter="ACTIVE")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='success').inc()
        except Exception as exc:
            logger.error(f"Error fetching campaigns: {exc}")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='error').inc()
            return 0

        logger.info(f"Collecting metrics for {len(campaigns)} campaigns")

        for campaign in campaigns:
            try:
                insights = await agent.get_campaign_insights(campaign['id'])
                if insights:
                    # TODO: Save to database in Sprint 4
                    # For now, just log
                    logger.info(
                        f"Collected insights for campaign {campaign['id']}: CTR={insights.get('ctr')}%")

                    campaigns_analyzed.inc()
                    facebook_api_calls.labels(
                        method='GET', status='success').inc()

            except Exception as e:
                logger.error(
                    f"Error collecting insights for campaign {campaign['id']}: {e}")
                facebook_api_calls.labels(
                    method='GET', status='error').inc()

        logger.info(
            f"Metrics collection completed for {len(campaigns)} campaigns")
        return len(campaigns)

    # Run async function
    return asyncio.run(_collect())
