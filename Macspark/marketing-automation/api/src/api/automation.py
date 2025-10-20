"""
Automation API Router
Endpoints para automações e otimizações
"""
from fastapi import APIRouter, HTTPException, Body, Depends, Request
from typing import Dict, Any, List

from src.agents.facebook_agent import FacebookAdsAgent
# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_cached_agent_provider
from src.automation.campaign_optimizer import CampaignOptimizer
from src.schemas.suggestion_schemas import SuggestionResponse
from src.utils.logger import setup_logger
from src.utils.auth import get_current_user
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)


@router.post("/pause-underperforming")
@limiter.limit("10/minute")
async def pause_underperforming(
    request: Request,
    ctr_threshold: float = Body(1.0, description="Minimum CTR threshold (%)"),
    cpa_threshold: float = Body(
        50.0, description="Maximum CPA threshold (R$)"),
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Generate pause suggestions for underperforming campaigns

    IMPORTANT: Only generates suggestions, does NOT pause automatically

    Args:
        ctr_threshold: Minimum acceptable CTR
        cpa_threshold: Maximum acceptable CPA

    Returns:
        List of pause suggestions
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        optimizer = CampaignOptimizer(
            ctr_threshold=ctr_threshold,
            cpa_threshold=cpa_threshold
        )

        # Get campaigns with insights
        campaigns = await agent.get_campaigns(status_filter="ACTIVE")
        campaigns_with_insights = []

        for campaign in campaigns:
            insights = await agent.get_campaign_insights(campaign['id'])
            if insights:
                campaigns_with_insights.append({
                    **campaign,
                    'insights': insights
                })

        # Evaluate and categorize
        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)

        # Generate pause suggestions
        suggestions = optimizer.generate_pause_suggestions(
            categorized['underperforming']
        )

        logger.info(f"Generated {len(suggestions)} pause suggestions")
        return suggestions

    except Exception as e:
        logger.error(f"Error in pause-underperforming: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize-budgets")
@limiter.limit("10/minute")
async def optimize_budgets(
    request: Request,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate budget optimization suggestions

    Returns:
        Budget adjustment suggestions (increase/decrease)
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        optimizer = CampaignOptimizer()

        # Get campaigns with insights
        campaigns = await agent.get_campaigns(status_filter="ACTIVE")
        campaigns_with_insights = []

        for campaign in campaigns[:20]:  # Limit to 20
            insights = await agent.get_campaign_insights(campaign['id'])
            if insights:
                campaigns_with_insights.append({
                    **campaign,
                    'insights': insights
                })

        # Evaluate
        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)

        # Generate budget suggestions
        budget_suggestions = optimizer.generate_budget_suggestions(categorized)

        logger.info(f"Generated {len(budget_suggestions)} budget suggestions")
        return {
            'suggestions': budget_suggestions,
            'summary': {
                'excellent_performers': len(categorized['excellent']),
                'good_performers': len(categorized['good']),
                'underperformers': len(categorized['underperforming'])
            }
        }

    except Exception as e:
        logger.error(f"Error optimizing budgets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggestions")
async def list_suggestions(
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    List all pending suggestions

    TODO: Implement database query in Sprint 4

    Returns:
        List of suggestions
    """
    return []


@router.post("/reallocation-plan")
async def generate_reallocation_plan(
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate intelligent budget reallocation plan

    Returns:
        Reallocation plan moving budget from underperformers to top performers
    """
    try:
        provider = get_cached_agent_provider()
        agent = provider.get_agent()
        optimizer = CampaignOptimizer()

        campaigns = await agent.get_campaigns(status_filter="ACTIVE")
        campaigns_with_insights = []

        for campaign in campaigns:
            insights = await agent.get_campaign_insights(campaign['id'])
            if insights:
                campaigns_with_insights.append({
                    **campaign,
                    'insights': insights
                })

        categorized = optimizer.evaluate_campaigns(campaigns_with_insights)
        plan = optimizer.generate_reallocation_plan(categorized)

        logger.info(f"Generated reallocation plan")
        return plan

    except Exception as e:
        logger.error(f"Error generating reallocation plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))
