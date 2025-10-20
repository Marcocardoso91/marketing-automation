"""
Notion API Router
Endpoints para integração com Notion
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any, List

from src.integrations.notion_client import get_notion_client
from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_cached_agent_provider
from src.analytics.performance_analyzer import PerformanceAnalyzer
from src.automation.campaign_optimizer import CampaignOptimizer
from src.utils.logger import setup_logger
from src.utils.auth import get_current_user
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/save-report/{campaign_id}")
@limiter.limit("20/minute")
async def save_campaign_report_to_notion(
    request: Request,
    campaign_id: str,
    database_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Salva relatório de campanha no Notion

    Args:
        campaign_id: ID da campanha Facebook
        database_id: ID do database Notion

    Returns:
        URL da página criada no Notion
    """
    try:
        # Buscar dados da campanha
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        analyzer = PerformanceAnalyzer()
        optimizer = CampaignOptimizer()

        campaigns = await agent.get_campaigns()
        campaign = next((c for c in campaigns if c['id'] == campaign_id), None)

        if not campaign:
            raise HTTPException(404, f"Campaign {campaign_id} not found")

        # Buscar insights
        insights = await agent.get_campaign_insights(campaign_id)
        if not insights:
            raise HTTPException(404, f"No insights for campaign {campaign_id}")

        # Calcular score
        score = analyzer.calculate_score(insights)

        # Gerar sugestões
        campaigns_with_insights = [{**campaign, 'insights': insights}]
        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)
        suggestions: List[Dict[str, Any]] = []

        underperforming_entry = next(
            (c for c in categorized['underperforming'] if c['id'] == campaign_id),
            None
        )
        excellent_entry = next(
            (c for c in categorized['excellent'] if c['id'] == campaign_id),
            None
        )

        if underperforming_entry:
            suggestions = optimizer.generate_pause_suggestions([underperforming_entry])
        elif excellent_entry:
            filtered_categorized = {
                'excellent': [excellent_entry],
                'good': [],
                'underperforming': []
            }
            suggestions = optimizer.generate_budget_suggestions(filtered_categorized)

        # Salvar no Notion
        notion_client = get_notion_client(database_id)
        page_url = await notion_client.create_campaign_report(
            campaign, insights, score, suggestions
        )

        return {
            "success": True,
            "notion_page_url": page_url,
            "campaign_id": campaign_id,
            "score": score
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving to Notion: {e}")
        raise HTTPException(500, str(e))


@router.post("/daily-summary")
@limiter.limit("20/minute")
async def create_daily_summary_notion(
    request: Request,
    database_id: str,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Cria sumário diário no Notion

    Args:
        database_id: ID do database Notion

    Returns:
        Resultado da criação
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        analyzer = PerformanceAnalyzer()
        optimizer = CampaignOptimizer()

        # Buscar campanhas
        campaigns = await agent.get_campaigns(status_filter="ACTIVE")

        total_spend = 0.0
        campaigns_with_insights = []

        for campaign in campaigns[:20]:
            insights = await agent.get_campaign_insights(campaign['id'], 'yesterday')
            if insights:
                score = analyzer.calculate_score(insights)
                total_spend += insights['spend']
                campaigns_with_insights.append({
                    **campaign,
                    'insights': insights,
                    'score': score
                })

        # Categorizar
        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)

        # Top performers (sorted by score)
        top_performers = sorted(
            categorized['good'] + categorized['excellent'],
            key=lambda x: x.get('score', 0),
            reverse=True
        )[:5]

        # Criar no Notion
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        notion_client = get_notion_client(database_id)
        page_url = await notion_client.create_daily_summary(
            date=yesterday,
            total_spend=total_spend,
            campaigns_analyzed=len(campaigns_with_insights),
            top_performers=top_performers,
            underperformers=categorized['underperforming']
        )

        return {
            "success": True,
            "notion_page_url": page_url,
            "date": yesterday,
            "total_spend": total_spend,
            "campaigns_analyzed": len(campaigns_with_insights)
        }

    except Exception as e:
        logger.error(f"Error creating daily summary: {e}")
        raise HTTPException(500, str(e))


@router.get("/search")
@limiter.limit("50/minute")
async def search_notion_reports(
    request: Request,
    query: str,
    database_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Busca relatórios no Notion

    Args:
        query: Termo de busca
        database_id: ID do database (opcional)

    Returns:
        Lista de páginas encontradas
    """
    try:
        # P0 #4 - Implemented real Notion search
        client = get_notion_client()
        results = await client.search_pages(query, database_id)
        logger.info(f"Found {len(results)} results for query: {query}")
        return results

    except Exception as e:
        logger.error(f"Error searching Notion: {e}")
        raise HTTPException(500, str(e))
