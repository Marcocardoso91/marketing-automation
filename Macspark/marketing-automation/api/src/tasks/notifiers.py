"""
Celery Tasks - Notifiers
"""
from src.tasks.celery_app import celery_app
from src.integrations.n8n_client import get_n8n_client
from src.utils.metrics import alerts_sent
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@celery_app.task(name='src.tasks.notifiers.send_alert')
def send_alert(campaign_data: dict, issue_type: str, severity: str = "WARNING"):
    """
    Send alert via n8n multi-channel

    Args:
        campaign_data: Campaign information
        issue_type: Type of issue
        severity: Alert severity
    """
    import asyncio

    async def _send():
        try:
            n8n_client = get_n8n_client()
            success = await n8n_client.send_alert(campaign_data, issue_type, severity)

            if success:
                alerts_sent.labels(channel='multi', severity=severity).inc()
                logger.info(
                    f"Alert sent for campaign {campaign_data.get('id')}")
            else:
                logger.error(
                    f"Failed to send alert for campaign {campaign_data.get('id')}")

            return success
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
            return False

    return asyncio.run(_send())
