"""
n8n Admin API Router
Gerenciamento de workflows n8n via MCP
"""
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, AnyHttpUrl, EmailStr

from src.integrations.n8n_manager import get_n8n_manager
from src.utils.logger import setup_logger
from src.utils.auth import get_current_user
from src.utils.rate_limit import limiter
from src.utils.exceptions import N8NConnectionError

router = APIRouter()
logger = setup_logger(__name__)


class CreateAlertsWorkflowPayload(BaseModel):
    slack_webhook: AnyHttpUrl
    email_from: EmailStr
    email_to: EmailStr


def _ensure_feature_available(identifier: str, result: Any) -> None:
    """Raise HTTP 501 when MCP integration is not available"""
    if result is None:
        raise HTTPException(
            status_code=501,
            detail=f"{identifier} is not available because n8n MCP integration is not enabled",
        )


@router.get("/workflows")
@limiter.limit("50/minute")
async def list_n8n_workflows(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Lista todos os workflows n8n

    Returns:
        Lista de workflows configurados
    """
    try:
        manager = get_n8n_manager()
        workflows = await manager.list_workflows()
        _ensure_feature_available("Workflow listing", workflows)
        return workflows

    except N8NConnectionError as exc:
        logger.error("n8n integration error: %s", exc.message)
        status = exc.details.get("status") if isinstance(exc.details, dict) else None
        raise HTTPException(
            status_code=status if isinstance(status, int) else 503,
            detail=exc.message,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing n8n workflows: {e}")
        raise HTTPException(500, str(e))


@router.post("/workflows/create-metrics")
@limiter.limit("10/minute")
async def create_metrics_workflow(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria workflow de coleta de métricas via MCP

    Returns:
        ID e detalhes do workflow criado
    """
    try:
        manager = get_n8n_manager()
        workflow_id = await manager.create_facebook_metrics_workflow()
        _ensure_feature_available("Metrics workflow creation", workflow_id)

        return {
            "success": True,
            "workflow_id": workflow_id,
            "workflow_name": "Facebook Fetch Metrics",
            "status": "created"
        }

    except N8NConnectionError as exc:
        logger.error("n8n integration error: %s", exc.message)
        status = exc.details.get("status") if isinstance(exc.details, dict) else None
        raise HTTPException(
            status_code=status if isinstance(status, int) else 503,
            detail=exc.message,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating metrics workflow: {e}")
        raise HTTPException(500, str(e))


@router.post("/workflows/create-alerts")
@limiter.limit("10/minute")
async def create_alerts_workflow(
    request: Request,
    payload: CreateAlertsWorkflowPayload,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria workflow de alertas multi-canal via MCP

    Returns:
        ID do workflow criado
    """
    try:
        manager = get_n8n_manager()

        email_config = {
            "fromEmail": payload.email_from,
            "toEmail": payload.email_to,
            "subject": "Facebook Ads Alert"
        }

        workflow_id = await manager.create_alert_workflow(
            payload.slack_webhook, email_config
        )
        _ensure_feature_available("Alert workflow creation", workflow_id)

        return {
            "success": True,
            "workflow_id": workflow_id,
            "workflow_name": "Send Alerts Multi-Channel",
            "channels": ["slack", "email"]
        }

    except N8NConnectionError as exc:
        logger.error("n8n integration error: %s", exc.message)
        status = exc.details.get("status") if isinstance(exc.details, dict) else None
        raise HTTPException(
            status_code=status if isinstance(status, int) else 503,
            detail=exc.message,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating alerts workflow: {e}")
        raise HTTPException(500, str(e))


@router.post("/workflows/{workflow_id}/validate")
@limiter.limit("20/minute")
async def validate_workflow(
    request: Request,
    workflow_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Valida configuração de um workflow

    Args:
        workflow_id: ID do workflow

    Returns:
        Resultado da validação
    """
    try:
        manager = get_n8n_manager()
        validation = await manager.validate_workflow(workflow_id)
        _ensure_feature_available("Workflow validation", validation)
        return validation

    except N8NConnectionError as exc:
        logger.error("n8n integration error: %s", exc.message)
        status = exc.details.get("status") if isinstance(exc.details, dict) else None
        raise HTTPException(
            status_code=status if isinstance(status, int) else 503,
            detail=exc.message,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating workflow: {e}")
        raise HTTPException(500, str(e))


@router.get("/nodes/search")
@limiter.limit("50/minute")
async def search_n8n_nodes(
    request: Request,
    query: str,
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Busca nodes n8n disponíveis
    """
    logger.info("Searching n8n nodes requested for query '%s'", query)
    raise HTTPException(
        status_code=501,
        detail="Node search via MCP is not available yet",
    )
