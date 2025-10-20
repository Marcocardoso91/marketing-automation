"""
Campaigns API Router
Endpoints para gerenciar campanhas do Facebook Ads
"""
from fastapi import APIRouter, HTTPException, Query, Request, Depends
from typing import List, Optional

from src.agents.facebook_agent import FacebookAdsAgent
from src.schemas.campaign_schemas import CampaignResponse, CampaignWithInsights
from src.utils.logger import setup_logger
from src.utils.rate_limit import limiter

router = APIRouter()
logger = setup_logger(__name__)

# Updated to use cached agent (P0 #5)
from src.utils.agent_cache import get_facebook_agent


@router.get("/", response_model=List[CampaignResponse])
@limiter.limit("100/minute")
async def list_campaigns(
    request: Request,
    status: Optional[str] = Query(
        None, description="Filter by status (ACTIVE, PAUSED, ALL)"),
    limit: int = Query(100, ge=1, le=500,
                       description="Max campaigns to return"),
    agent: FacebookAdsAgent = Depends(get_facebook_agent)
):
    """
    List Facebook Ads campaigns

    Args:
        status: Filter by campaign status
        limit: Maximum number of campaigns

    Returns:
        List of campaigns
    """
    try:
        campaigns = await agent.get_campaigns(status_filter=status, limit=limit)
        return campaigns
    except Exception as e:
        logger.error(f"Error listing campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    agent: FacebookAdsAgent = Depends(get_facebook_agent)
):
    """
    Get campaign details

    Args:
        campaign_id: Facebook campaign ID

    Returns:
        Campaign details
    """
    try:
        campaigns = await agent.get_campaigns()

        campaign = next((c for c in campaigns if c['id'] == campaign_id), None)
        if not campaign:
            raise HTTPException(
                status_code=404, detail=f"Campaign {campaign_id} not found")

        return campaign
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching campaign {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/insights")
async def get_campaign_insights(
    campaign_id: str,
    date_preset: str = Query(
        "last_7d", description="Date range (last_7d, last_14d, last_30d, today)"),
    agent: FacebookAdsAgent = Depends(get_facebook_agent)
):
    """
    Get campaign insights/metrics

    Args:
        campaign_id: Facebook campaign ID
        date_preset: Date range preset

    Returns:
        Campaign metrics
    """
    try:
        insights = await agent.get_campaign_insights(campaign_id, date_preset)

        if not insights:
            raise HTTPException(
                status_code=404, detail=f"No insights found for campaign {campaign_id}")

        return insights
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching insights for {campaign_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
