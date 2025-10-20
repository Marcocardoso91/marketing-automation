"""
Endpoints de exportação de métricas para sistema de analytics.
"""
from fastapi import APIRouter, Header, HTTPException, Query, Depends, Request
from datetime import date as DateType, datetime
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from marketing_shared.schemas.facebook_metrics import (
    CampaignMetricSchema,
    ExportedMetricsResponse
)
from src.utils.config import settings
from src.agents.facebook_agent import FacebookAdsAgent
from src.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_facebook_agent


def verify_analytics_api_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Verifica se API key é válida"""
    if api_key != settings.ANALYTICS_API_KEY:
        logger.warning(f"Tentativa de acesso com API key inválida")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@router.get("/export", response_model=ExportedMetricsResponse)
@limiter.limit("1000/hour")  # Rate limit generoso para analytics
async def export_metrics(
    request: Request,
    date_from: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="Data inicial (YYYY-MM-DD)"),
    date_until: str = Query(..., pattern=r'^\d{4}-\d{2}-\d{2}$', description="Data final (YYYY-MM-DD)"),
    api_key: str = Depends(verify_analytics_api_key),
    agent: FacebookAdsAgent = Depends(get_facebook_agent)
):
    """
    Exporta métricas Meta Ads para sistema de analytics.
    
    **Autenticação:** Header X-API-Key  
    **Rate Limit:** 1000 requests/hora  
    **Formato:** JSON (ExportedMetricsResponse)
    
    **Exemplo:**
    ```bash
    curl -H "X-API-Key: your_key" \\
         "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-18&date_until=2025-10-18"
    ```
    """
    logger.info(f"Exportando métricas de {date_from} até {date_until}")
    
    try:
        # Parse e validação das datas
        start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_until, "%Y-%m-%d").date()

        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="`date_from` deve ser menor ou igual a `date_until`"
            )

        campaigns_raw = await agent.get_campaigns(status_filter="ACTIVE")
        campaigns: List[CampaignMetricSchema] = []

        for campaign in campaigns_raw:
            insights = await agent.get_campaign_insights(
                campaign_id=campaign["id"],
                date_from=start_date.isoformat(),
                date_until=end_date.isoformat()
            )

            if not insights:
                continue

            conversions = int(insights.get("purchases", 0))
            clicks = int(insights.get("clicks", 0))
            ctr_value = float(insights.get("ctr", 0) or 0)
            cpc_value = float(insights.get("cpc", 0) or 0)
            frequency = float(insights.get("frequency", 0) or 0)
            date_start = insights.get("date_start") or start_date.isoformat()
            metric_date = datetime.strptime(date_start, "%Y-%m-%d").date()

            conversion_rate = None
            if clicks > 0 and conversions > 0:
                conversion_rate = (conversions / clicks) * 100

            campaigns.append(
                CampaignMetricSchema(
                    campaign_id=str(campaign["id"]),
                    campaign_name=campaign["name"],
                    date=metric_date,
                    impressions=int(insights.get("impressions", 0)),
                    clicks=clicks,
                    spend=float(insights.get("spend", 0) or 0.0),
                    reach=int(insights.get("reach", 0) or 0),
                    frequency=frequency,
                    ctr=ctr_value,
                    cpc=cpc_value,
                    cpe=None,
                    cpm=float(insights.get("cpm", 0) or 0),
                    conversions=conversions,
                    conversion_rate=conversion_rate,
                    roas=insights.get("roas"),
                )
            )
        
        logger.info(f"✅ Exportadas {len(campaigns)} campanhas com sucesso")
        
        return ExportedMetricsResponse(
            campaigns=campaigns,
            total_campaigns=len(campaigns),
            date_from=start_date,
            date_until=end_date,
            exported_at=datetime.utcnow(),
            data_source="facebook-ads-ai-agent",
            version="1.0.0"
        )
        
    except HTTPException:
        raise
    except ValueError as err:
        logger.error(f"Erro de validação de datas: {err}")
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as e:
        logger.error(f"❌ Erro ao exportar métricas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar métricas: {str(e)}")


@router.get("/health")
async def health():
    """Health check do endpoint de métricas"""
    return {
        "status": "healthy",
        "endpoint": "metrics",
        "version": "1.0.0"
    }

