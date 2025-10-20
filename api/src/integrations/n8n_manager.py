"""
n8n Manager
Gerenciamento programático de workflows n8n via MCP
"""
from typing import Dict, Any, List, Optional
import os
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class N8nWorkflowManager:
    """
    Gerenciador para criar e configurar workflows n8n programaticamente

    Usa o MCP n8n para:
    - Criar workflows
    - Validar configurações
    - Listar workflows existentes
    - Executar workflows via webhook

    Conectado à instância Macspark: https://fluxos.macspark.dev
    """

    def __init__(self):
        """Initialize n8n manager"""
        self.api_url = os.getenv(
            "N8N_API_URL", "https://fluxos.macspark.dev/api/v1")
        self.api_key = os.getenv("N8N_API_KEY")
        self.webhook_url = os.getenv(
            "N8N_WEBHOOK_URL", "https://fluxos.macspark.dev/webhook")

        if not self.api_key:
            logger.warning("N8N_API_KEY not configured")
        else:
            logger.info(
                f"N8nManager initialized with Macspark instance: {self.api_url}")

    async def create_facebook_metrics_workflow(self) -> Optional[str]:
        """
        Cria workflow de coleta de métricas Facebook

        Returns:
            ID do workflow criado ou None
        """
        try:
            workflow_config = {
                "name": "Facebook Fetch Metrics",
                "active": True,
                "nodes": [
                    {
                        "id": "webhook-trigger",
                        "name": "Webhook Trigger",
                        "type": "n8n-nodes-base.webhook",
                        "parameters": {
                            "path": "fb_fetch_metrics",
                            "responseMode": "responseNode"
                        },
                        "position": [250, 300]
                    },
                    {
                        "id": "http-facebook",
                        "name": "Facebook API Call",
                        "type": "n8n-nodes-base.httpRequest",
                        "parameters": {
                            "url": "https://graph.facebook.com/v18.0/{{ $json.account_id }}/campaigns",
                            "method": "GET",
                            "options": {
                                "queryParameters": {
                                    "parameters": [
                                        {
                                            "name": "fields",
                                            "value": "id,name,status,insights{impressions,clicks,spend}"
                                        }
                                    ]
                                }
                            }
                        },
                        "position": [450, 300]
                    },
                    {
                        "id": "transform",
                        "name": "Transform Data",
                        "type": "n8n-nodes-base.code",
                        "parameters": {
                            "jsCode": "return $input.all()[0].json.data;"
                        },
                        "position": [650, 300]
                    }
                ],
                "connections": {
                    "Webhook Trigger": {
                        "main": [[{"node": "Facebook API Call", "type": "main", "index": 0}]]
                    },
                    "Facebook API Call": {
                        "main": [[{"node": "Transform Data", "type": "main", "index": 0}]]
                    }
                }
            }

            logger.warning("n8n MCP integration not available; returning placeholder response")
            return None

        except Exception as e:
            logger.error(f"Erro ao criar workflow n8n: {e}")
            return None

    async def create_alert_workflow(
        self,
        slack_webhook: str,
        email_config: Dict[str, str]
    ) -> Optional[str]:
        """
        Cria workflow de alertas multi-canal

        Args:
            slack_webhook: URL do webhook Slack
            email_config: Configuração SMTP

        Returns:
            ID do workflow criado
        """
        try:
            workflow_config = {
                "name": "Send Alerts Multi-Channel",
                "active": True,
                "nodes": [
                    {
                        "id": "webhook",
                        "name": "Webhook",
                        "type": "n8n-nodes-base.webhook",
                        "parameters": {
                            "path": "send_alerts_multi"
                        }
                    },
                    {
                        "id": "slack",
                        "name": "Slack",
                        "type": "n8n-nodes-base.slack",
                        "parameters": {
                            "webhook_url": slack_webhook,
                            "text": "⚠️ Alert: {{ $json.issue_type }}\nCampaign: {{ $json.campaign_name }}"
                        }
                    },
                    {
                        "id": "email",
                        "name": "Email",
                        "type": "n8n-nodes-base.emailSend",
                        "parameters": email_config
                    }
                ]
            }

            logger.warning("n8n MCP integration not available; returning placeholder response")
            return None

        except Exception as e:
            logger.error(f"Erro ao criar workflow alertas: {e}")
            return None

    async def list_workflows(self) -> List[Dict[str, Any]]:
        """
        Lista todos os workflows n8n

        Returns:
            Lista de workflows
        """
        try:
            logger.info("Listando workflows n8n via MCP (não implementado)")
            return []
        except Exception as e:
            logger.error(f"Erro ao listar workflows: {e}")
            return []

    async def validate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Valida configuração de workflow

        Args:
            workflow_id: ID do workflow

        Returns:
            Resultado da validação
        """
        try:
            logger.info(f"Validando workflow {workflow_id} via MCP (não implementado)")
            return {"valid": False, "errors": ["MCP validation not implemented"]}
        except Exception as e:
            logger.error(f"Erro ao validar workflow: {e}")
            return {"valid": False, "errors": [str(e)]}


# Singleton
_n8n_manager = None


def get_n8n_manager() -> N8nWorkflowManager:
    """Get singleton n8n manager"""
    global _n8n_manager
    if _n8n_manager is None:
        _n8n_manager = N8nWorkflowManager()
    return _n8n_manager
