"""
n8n Manager
Gerenciamento programático de workflows n8n via MCP
"""
from typing import Dict, Any, List, Optional
import os

import httpx

from src.utils.exceptions import N8NConnectionError
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class N8nWorkflowManager:
    """
    Gerenciador para criar e configurar workflows n8n programaticamente.

    Os métodos realizam chamadas HTTP diretas para a API do n8n utilizando a
    `N8N_API_KEY`. Quando a integração não estiver configurada, um
    `N8NConnectionError` será lançado para que a camada FastAPI responda com
    erro apropriado (HTTP 503/502).
    """

    def __init__(self):
        """Initialize n8n manager"""
        self.api_url = os.getenv(
            "N8N_API_URL", "https://fluxos.macspark.dev/api/v1"
        ).rstrip("/")
        self.api_key = os.getenv("N8N_API_KEY")
        self.webhook_url = os.getenv(
            "N8N_WEBHOOK_URL", "https://fluxos.macspark.dev/webhook"
        ).rstrip("/")
        self.timeout = float(os.getenv("N8N_API_TIMEOUT", "30"))

        if not self.api_key:
            logger.warning("N8N_API_KEY not configured – MCP endpoints will return 503")
        else:
            logger.info(
                "N8nManager inicializado com instância %s", self.api_url
            )

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _ensure_configured(self) -> None:
        if not self.api_key:
            raise N8NConnectionError(
                message="N8N_API_KEY is not configured; enable n8n integration first"
            )

    def _headers(self) -> Dict[str, str]:
        return {
            "X-N8N-API-KEY": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        self._ensure_configured()
        url = f"{self.api_url}{path if path.startswith('/') else f'/{path}'}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self._headers(),
                    **kwargs,
                )
                response.raise_for_status()
                if not response.content:
                    return None
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "n8n API error (%s %s): %s",
                method,
                url,
                exc.response.text,
            )
            raise N8NConnectionError(
                message=f"n8n API error ({exc.response.status_code})",
                details={"status": exc.response.status_code},
            ) from exc
        except httpx.RequestError as exc:
            logger.error("Failed to reach n8n API: %s", exc)
            raise N8NConnectionError(
                message="Unable to reach n8n API",
                details={"error": str(exc)},
            ) from exc

    def _extract_workflow_id(self, payload: Optional[Dict[str, Any]]) -> Optional[str]:
        if not payload:
            return None
        if "data" in payload and isinstance(payload["data"], dict):
            return payload["data"].get("id")
        return payload.get("id")

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    async def create_facebook_metrics_workflow(self) -> Optional[str]:
        """
        Cria workflow de coleta de métricas Facebook e retorna o ID criado.
        """
        workflow_config = {
            "name": "Facebook Fetch Metrics",
            "active": True,
            "nodes": [
                {
                    "name": "Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "parameters": {
                        "path": "fb_fetch_metrics",
                        "responseMode": "responseNode",
                    },
                },
                {
                    "name": "Facebook API Call",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [450, 300],
                    "parameters": {
                        "url": (
                            "https://graph.facebook.com/v18.0/"
                            "{{ $json.account_id }}/campaigns"
                        ),
                        "method": "GET",
                        "options": {
                            "queryParameters": {
                                "parameters": [
                                    {
                                        "name": "fields",
                                        "value": (
                                            "id,name,status,"
                                            "insights{impressions,clicks,spend}"
                                        ),
                                    }
                                ]
                            }
                        },
                    },
                },
                {
                    "name": "Transform Data",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 1,
                    "position": [650, 300],
                    "parameters": {
                        "jsCode": "return $input.all()[0].json.data;",
                    },
                },
            ],
            "connections": {
                "Webhook Trigger": {
                    "main": [[{"node": "Facebook API Call", "type": "main", "index": 0}]]
                },
                "Facebook API Call": {
                    "main": [[{"node": "Transform Data", "type": "main", "index": 0}]]
                },
            },
        }

        payload = await self._request("POST", "/workflows", json=workflow_config)
        workflow_id = self._extract_workflow_id(payload)
        logger.info("Created n8n workflow %s", workflow_id)
        return workflow_id

    async def create_alert_workflow(
        self,
        slack_webhook: str,
        email_config: Dict[str, str],
    ) -> Optional[str]:
        """
        Cria workflow de alertas multi-canal e retorna o ID.
        """
        workflow_config = {
            "name": "Send Alerts Multi-Channel",
            "active": True,
            "nodes": [
                {
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "parameters": {"path": "send_alerts_multi"},
                },
                {
                    "name": "Slack",
                    "type": "n8n-nodes-base.slack",
                    "typeVersion": 1,
                    "position": [450, 300],
                    "parameters": {
                        "webhookUrl": slack_webhook,
                        "text": (
                            "⚠️ Alert: {{ $json.issue_type }}\n"
                            "Campaign: {{ $json.campaign_name }}"
                        ),
                    },
                },
                {
                    "name": "Email",
                    "type": "n8n-nodes-base.emailSend",
                    "typeVersion": 1,
                    "position": [650, 300],
                    "parameters": email_config,
                },
            ],
            "connections": {
                "Webhook": {
                    "main": [[{"node": "Slack", "type": "main", "index": 0}]]
                },
                "Slack": {
                    "main": [[{"node": "Email", "type": "main", "index": 0}]]
                },
            },
        }

        payload = await self._request("POST", "/workflows", json=workflow_config)
        workflow_id = self._extract_workflow_id(payload)
        logger.info("Created alert workflow %s", workflow_id)
        return workflow_id

    async def list_workflows(self) -> List[Dict[str, Any]]:
        """
        Lista workflows disponíveis na instância n8n configurada.
        """
        payload = await self._request("GET", "/workflows")
        if not payload:
            return []
        data = payload.get("data")
        if isinstance(data, list):
            return data
        if isinstance(payload, list):
            return payload
        return []

    async def validate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Obtém detalhes do workflow indicado e retorna um resumo simples.
        """
        payload = await self._request("GET", f"/workflows/{workflow_id}")
        if not payload:
            return {"valid": False, "errors": ["Workflow not found"]}

        data = payload.get("data") if isinstance(payload, dict) else payload
        workflow = data if isinstance(data, dict) else payload
        is_active = bool(workflow.get("active")) if isinstance(workflow, dict) else False

        return {
            "valid": True,
            "workflow_id": workflow.get("id"),
            "name": workflow.get("name"),
            "active": is_active,
        }


# Singleton
_n8n_manager = None


def get_n8n_manager() -> N8nWorkflowManager:
    """Get singleton n8n manager"""
    global _n8n_manager
    if _n8n_manager is None:
        _n8n_manager = N8nWorkflowManager()
    return _n8n_manager
