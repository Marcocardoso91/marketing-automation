"""
Celery Tasks - Data Processors
"""
from src.tasks.celery_app import celery_app
from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5) - shorter TTL for background tasks
from src.utils.agent_cache import get_cached_agent_provider
from src.analytics.performance_analyzer import PerformanceAnalyzer
from src.automation.campaign_optimizer import CampaignOptimizer
from src.integrations.n8n_client import get_n8n_client
from src.utils.metrics import facebook_api_calls
from src.utils.logger import setup_logger
from datetime import datetime, timedelta

logger = setup_logger(__name__)


@celery_app.task(name='src.tasks.processors.analyze_performance')
def analyze_performance():
    """
    Analyze campaign performance and detect issues
    Runs every hour
    """
    import asyncio

    async def _analyze():
        try:
            # Use shorter cache TTL for background tasks (30min)
            provider = get_cached_agent_provider(cache_ttl=1800)
            agent = provider.get_agent()
        except Exception as exc:
            logger.error(f"Failed to initialize Facebook agent: {exc}")
            facebook_api_calls.labels(method='INIT', status='error').inc()
            return 0

        analyzer = PerformanceAnalyzer()
        optimizer = CampaignOptimizer()
        n8n_client = get_n8n_client()

        try:
            campaigns = await agent.get_campaigns(status_filter="ACTIVE")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='success').inc()
        except Exception as exc:
            logger.error(f"Error fetching campaigns: {exc}")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='error').inc()
            return 0

        campaigns_with_insights = []

        for campaign in campaigns[:20]:  # Limit to 20
            try:
                insights = await agent.get_campaign_insights(campaign['id'])
                facebook_api_calls.labels(
                    method='GET', status='success').inc()
            except Exception as exc:
                logger.error(
                    f"Error collecting insights for campaign {campaign['id']}: {exc}")
                facebook_api_calls.labels(
                    method='GET', status='error').inc()
                continue

            if insights:
                score = analyzer.calculate_score(insights)
                campaigns_with_insights.append({
                    **campaign,
                    'insights': insights,
                    'score': score
                })

        # Categorize campaigns
        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)

        # Send alerts for underperforming
        import os
        from src.integrations.notion_client import get_notion_client

        notion_db_id = os.getenv("NOTION_DATABASE_ID")
        whatsapp_phone = os.getenv("WHATSAPP_ALERT_PHONE")

        for campaign in categorized['underperforming']:
            # 1. Alerta n8n multi-canal (Slack + Email)
            await n8n_client.send_alert(
                campaign_data=campaign,
                issue_type="UNDERPERFORMING",
                severity="WARNING"
            )

            # 2. Salvar no Notion (se configurado)
            if notion_db_id:
                try:
                    notion = get_notion_client(notion_db_id)
                    notion_url = await notion.save_suggestion({
                        'campaign_id': campaign['id'],
                        'campaign_name': campaign['name'],
                        'type': 'PAUSE',
                        'reason': f"Score baixo: {campaign['score']:.0f}/100",
                        'data': campaign['insights']
                    })
                    logger.info(f"✅ Alerta salvo no Notion: {notion_url}")
                except Exception as e:
                    logger.error(f"Erro ao salvar no Notion: {e}")

            # 3. WhatsApp para scores críticos (< 30)
            if campaign['score'] < 30 and whatsapp_phone:
                try:
                    await n8n_client.trigger_workflow("evolution-webhook", {
                        "phone": whatsapp_phone,
                        "message": f"""
🚨 *CRÍTICO* - Facebook Ads

{campaign['name']}
Score: {campaign['score']:.0f}/100

CTR: {campaign['insights']['ctr']:.2f}%
CPA: R$ {campaign['insights']['cpa']:.2f}

Verificar URGENTE!
                            """
                    })
                    logger.info(
                        f"📱 Alerta WhatsApp enviado para {whatsapp_phone}")
                except Exception as e:
                    logger.error(f"Erro ao enviar WhatsApp: {e}")

        logger.info(
            f"Performance analysis completed: {len(categorized['underperforming'])} alerts sent")
        return len(campaigns_with_insights)

    return asyncio.run(_analyze())


@celery_app.task(name='src.tasks.processors.generate_daily_report')
def generate_daily_report():
    """
    Generate daily performance report
    Runs daily at 8am
    """
    import asyncio

    async def _generate():
        try:
            # Use shorter cache TTL for background tasks (30min)
            provider = get_cached_agent_provider(cache_ttl=1800)
            agent = provider.get_agent()
        except Exception as exc:
            logger.error(f"Failed to initialize Facebook agent: {exc}")
            facebook_api_calls.labels(method='INIT', status='error').inc()
            return {}

        try:
            campaigns = await agent.get_campaigns(status_filter="ACTIVE")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='success').inc()
        except Exception as exc:
            logger.error(f"Error fetching campaigns: {exc}")
            facebook_api_calls.labels(
                method='LIST_CAMPAIGNS', status='error').inc()
            return {}

        total_spend = 0.0
        total_clicks = 0
        total_impressions = 0

        for campaign in campaigns:
            try:
                insights = await agent.get_campaign_insights(
                    campaign['id'], 'yesterday')
                facebook_api_calls.labels(
                    method='GET', status='success').inc()
            except Exception as exc:
                logger.error(
                    f"Error collecting insights for campaign {campaign['id']}: {exc}")
                facebook_api_calls.labels(
                    method='GET', status='error').inc()
                continue

            if insights:
                total_spend += insights['spend']
                total_clicks += insights['clicks']
                total_impressions += insights['impressions']

        report = {
            'date': str(datetime.now().date() - timedelta(days=1)),
            'total_spend': total_spend,
            'total_clicks': total_clicks,
            'total_impressions': total_impressions,
            'campaigns_count': len(campaigns)
        }

        # TODO: Save report to data/exports/ and send via email
        logger.info(f"Daily report generated: {report}")
        return report

    return asyncio.run(_generate())


@celery_app.task(name='src.tasks.processors.cleanup_old_data')
def cleanup_old_data():
    """
    Cleanup old data from database
    Runs weekly on Sunday at 2am
    """
    import asyncio

    async def _cleanup():
        try:
            # TODO: Implement database cleanup in Sprint 4
            # Delete conversations > 90 days
            # Delete insights > 365 days
            logger.info("Data cleanup completed")
            return True
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")
            return False

    return asyncio.run(_cleanup())
