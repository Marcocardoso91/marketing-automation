"""
Analytics API Router
Endpoints para análise de performance
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any

from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_cached_agent_provider
from src.analytics.performance_analyzer import PerformanceAnalyzer
from src.utils.logger import setup_logger
from src.utils.auth import get_current_user
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)


@router.get("/dashboard")
@limiter.limit("30/minute")
async def get_dashboard(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get dashboard summary data

    Returns:
        Dashboard with summary metrics and top campaigns
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        campaigns = await agent.get_campaigns(status_filter="ACTIVE")

        total_spend = 0.0
        total_clicks = 0
        total_impressions = 0
        ctr_values = []
        cpc_values = []

        campaigns_with_metrics = []

        for campaign in campaigns[:20]:  # Limit to 20 for performance
            insights = await agent.get_campaign_insights(campaign['id'])
            if insights:
                total_spend += insights['spend']
                total_clicks += insights['clicks']
                total_impressions += insights['impressions']

                if insights['ctr'] > 0:
                    ctr_values.append(insights['ctr'])
                if insights['cpc'] > 0:
                    cpc_values.append(insights['cpc'])

                campaigns_with_metrics.append({
                    **campaign,
                    'metrics': insights
                })

        avg_ctr = sum(ctr_values) / len(ctr_values) if ctr_values else 0.0
        avg_cpc = sum(cpc_values) / len(cpc_values) if cpc_values else 0.0

        # Sort campaigns by spend
        top_campaigns = sorted(
            campaigns_with_metrics,
            key=lambda x: x['metrics']['spend'],
            reverse=True
        )[:10]

        return {
            'summary': {
                'total_spend': round(total_spend, 2),
                'total_clicks': total_clicks,
                'total_impressions': total_impressions,
                'average_ctr': round(avg_ctr, 2),
                'average_cpc': round(avg_cpc, 2),
                'active_campaigns_count': len(campaigns)
            },
            'top_campaigns': top_campaigns
        }
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance")
@limiter.limit("30/minute")
async def get_performance_analysis(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed performance analysis with scores

    Returns:
        Performance analysis for all campaigns
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        analyzer = PerformanceAnalyzer()

        campaigns = await agent.get_campaigns(status_filter="ACTIVE")
        analysis = []

        for campaign in campaigns[:15]:  # Limit to 15
            insights = await agent.get_campaign_insights(campaign['id'])
            if insights:
                score = analyzer.calculate_score(insights)

                analysis.append({
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign['name'],
                    'score': score,
                    'metrics': insights,
                    'rating': 'Excelente' if score >= 80 else 'Bom' if score >= 60 else 'Regular' if score >= 40 else 'Ruim'
                })

        # Sort by score descending
        analysis.sort(key=lambda x: x['score'], reverse=True)

        return {
            'campaigns': analysis,
            'timestamp': str(datetime.now())
        }
    except Exception as e:
        logger.error(f"Error in performance analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends")
@limiter.limit("30/minute")
async def get_trends(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get performance trends over time

    Returns:
        Trend analysis for different periods
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        analyzer = PerformanceAnalyzer()

        campaigns = await agent.get_campaigns(status_filter="ACTIVE", limit=10)

        all_insights_7d = []
        all_insights_14d = []
        all_insights_30d = []

        for campaign in campaigns:
            insights_7d = await agent.get_campaign_insights(campaign['id'], 'last_7d')
            insights_14d = await agent.get_campaign_insights(campaign['id'], 'last_14d')
            insights_30d = await agent.get_campaign_insights(campaign['id'], 'last_30d')

            if insights_7d:
                all_insights_7d.append(insights_7d)
            if insights_14d:
                all_insights_14d.append(insights_14d)
            if insights_30d:
                all_insights_30d.append(insights_30d)

        trends = analyzer.analyze_trends(
            all_insights_7d, all_insights_14d, all_insights_30d)

        return {
            'trends': trends,
            'campaigns_analyzed': len(campaigns)
        }
    except Exception as e:
        logger.error(f"Error analyzing trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Import datetime
