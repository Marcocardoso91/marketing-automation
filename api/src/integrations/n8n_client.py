"""
n8n Client
Cliente para integração com n8n workflows
"""
from typing import List
from datetime import datetime
import httpx
from typing import Dict, Any, Optional
from src.utils.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class N8nClient:
    """
    Cliente para interagir com n8n workflows via webhooks
    """

    def __init__(self):
        """Initialize n8n client"""
        self.base_url = settings.N8N_WEBHOOK_URL
        self.timeout = 30.0

    async def trigger_workflow(
        self,
        workflow_name: str,
        payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger n8n workflow via webhook

        Args:
            workflow_name: Name of the workflow
            payload: Data to send to workflow

        Returns:
            Response from n8n or None if error
        """
        try:
            url = f"{self.base_url}/{workflow_name}"

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                logger.info(f"Triggered n8n workflow: {workflow_name}")
                return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error triggering workflow {workflow_name}: {e}")
            return None
        except httpx.RequestError as e:
            logger.error(
                f"Request error triggering workflow {workflow_name}: {e}")
            return None
        except Exception as e:
            logger.error(
                f"Unexpected error triggering workflow {workflow_name}: {e}")
            return None

    async def send_alert(
        self,
        campaign_data: Dict[str, Any],
        issue_type: str,
        severity: str = "WARNING"
    ) -> bool:
        """
        Send alert via n8n workflow (multi-channel)

        Args:
            campaign_data: Campaign information
            issue_type: Type of issue (CTR_BAIXO, CPA_ALTO, etc.)
            severity: Alert severity (INFO, WARNING, CRITICAL)

        Returns:
            True if successful, False otherwise
        """
        payload = {
            'campaign_id': campaign_data.get('id'),
            'campaign_name': campaign_data.get('name'),
            'issue_type': issue_type,
            'severity': severity,
            'metrics': campaign_data.get('insights', {}),
            'timestamp': str(datetime.now())
        }

        result = await self.trigger_workflow('send_alerts_multi', payload)
        return result is not None

    async def fetch_metrics_async(
        self,
        account_id: str,
        campaign_ids: Optional[List[str]] = None
    ) -> bool:
        """
        Trigger async metrics collection via n8n

        Args:
            account_id: Facebook Ad Account ID
            campaign_ids: Optional list of specific campaigns

        Returns:
            True if triggered successfully
        """
        payload = {
            'account_id': account_id,
            'campaign_ids': campaign_ids or [],
            'timestamp': str(datetime.now())
        }

        result = await self.trigger_workflow('fb_fetch_metrics', payload)
        return result is not None

    async def get_calendar_context(
        self,
        date_range_days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Get calendar context for upcoming events

        Args:
            date_range_days: Number of days ahead to look

        Returns:
            Calendar events or None
        """
        payload = {
            'date_range_days': date_range_days,
            'timestamp': str(datetime.now())
        }

        return await self.trigger_workflow('calendar_context', payload)


# Singleton
_n8n_client = None


def get_n8n_client() -> N8nClient:
    """Get singleton n8n client instance"""
    global _n8n_client
    if _n8n_client is None:
        _n8n_client = N8nClient()
    return _n8n_client


# Import datetime
