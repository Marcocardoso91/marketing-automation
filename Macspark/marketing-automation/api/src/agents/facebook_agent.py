"""
Facebook Ads Agent
Main intelligent agent for Facebook Ads campaign management
"""
from typing import List, Dict, Any, Optional
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign as FBCampaign
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from datetime import datetime, timedelta

from src.utils.config import settings
from src.utils.logger import setup_logger
from src.utils.api_client import get_api_client
from src.utils.token_manager import get_token_manager
from src.analytics.performance_analyzer import PerformanceAnalyzer
from src.automation.campaign_optimizer import CampaignOptimizer

logger = setup_logger(__name__)


class FacebookAdsAgent:
    """
    Main agent for Facebook Ads operations

    Capabilities:
    - Fetch campaigns and insights
    - Process natural language queries
    - Generate performance analysis
    """

    def __init__(self):
        """Initialize Facebook Ads Agent"""
        self.token_manager = get_token_manager()
        self.api_client = get_api_client()
        self.app_id = settings.FACEBOOK_APP_ID
        self.app_secret = settings.FACEBOOK_APP_SECRET
        self.access_token = settings.FACEBOOK_ACCESS_TOKEN
        self.ad_account_id = settings.FACEBOOK_AD_ACCOUNT_ID

        # Initialize specialized components
        self.performance_analyzer = PerformanceAnalyzer()
        self.campaign_optimizer = CampaignOptimizer()

        self._init_facebook_api()

        logger.info("FacebookAdsAgent initialized successfully")

    def _init_facebook_api(self):
        """Initialize Facebook Marketing API"""
        try:
            token = self.token_manager.get_valid_token()
            FacebookAdsApi.init(
                self.app_id,
                self.app_secret,
                token
            )
            self.account = AdAccount(self.ad_account_id)
            logger.info(
                f"Facebook API initialized for account {self.ad_account_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Facebook API: {e}")
            raise

    async def get_campaigns(
        self,
        status_filter: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch campaigns from Facebook Ads

        Args:
            status_filter: Filter by status (ACTIVE, PAUSED, etc.)
            limit: Maximum number of campaigns to return

        Returns:
            List of campaigns with basic info
        """
        try:
            params = {
                'limit': limit,
            }

            if status_filter and status_filter != "ALL":
                params['filtering'] = [
                    {'field': 'status', 'operator': 'IN',
                        'value': [status_filter]}
                ]

            fields = [
                FBCampaign.Field.id,
                FBCampaign.Field.name,
                FBCampaign.Field.status,
                FBCampaign.Field.objective,
                FBCampaign.Field.daily_budget,
                FBCampaign.Field.lifetime_budget,
                FBCampaign.Field.created_time,
                FBCampaign.Field.updated_time,
            ]

            campaigns = await self.api_client.execute_with_retry(
                self.account.get_campaigns,
                fields=fields,
                params=params
            )

            result = []
            synced_at = datetime.utcnow()
            for campaign in campaigns:
                result.append({
                    'id': campaign.get('id'),
                    'name': campaign.get('name'),
                    'status': campaign.get('status'),
                    'objective': campaign.get('objective'),
                    'daily_budget': campaign.get('daily_budget'),
                    'lifetime_budget': campaign.get('lifetime_budget'),
                    'created_time': campaign.get('created_time'),
                    'updated_time': campaign.get('updated_time'),
                    'synced_at': synced_at,
                })

            logger.info(f"Fetched {len(result)} campaigns")
            return result

        except Exception as e:
            logger.error(f"Error fetching campaigns: {e}")
            raise

    async def get_campaign_insights(
        self,
        campaign_id: str,
        date_preset: str = 'last_7d',
        date_from: Optional[str] = None,
        date_until: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch insights for a specific campaign

        Args:
            campaign_id: Facebook campaign ID
            date_preset: Date range preset (last_7d, last_14d, last_30d)
            date_from: Optional start date (YYYY-MM-DD)
            date_until: Optional end date (YYYY-MM-DD)

        Returns:
            Campaign insights with metrics or None if no data
        """
        try:
            campaign = FBCampaign(campaign_id)

            params = {'level': 'campaign'}

            if date_from and date_until:
                params['time_range'] = {'since': date_from, 'until': date_until}
            else:
                params['date_preset'] = date_preset

            fields = [
                AdsInsights.Field.impressions,
                AdsInsights.Field.clicks,
                AdsInsights.Field.spend,
                AdsInsights.Field.reach,
                AdsInsights.Field.frequency,
                AdsInsights.Field.ctr,
                AdsInsights.Field.cpc,
                AdsInsights.Field.cpm,
                AdsInsights.Field.actions,
                AdsInsights.Field.date_start,
                AdsInsights.Field.date_stop,
            ]

            insights = await self.api_client.execute_with_retry(
                campaign.get_insights,
                fields=fields,
                params=params
            )

            if not insights:
                return None

            insight_data = insights[0]

            # Extract purchase actions
            purchases = 0
            if 'actions' in insight_data:
                for action in insight_data['actions']:
                    if action.get('action_type') == 'purchase':
                        purchases = int(action.get('value', 0))

            # Calculate CPA if purchases > 0
            spend = float(insight_data.get('spend', 0))
            cpa = (spend / purchases) if purchases > 0 else None

            result = {
                'campaign_id': campaign_id,
                'date_start': insight_data.get('date_start'),
                'date_stop': insight_data.get('date_stop'),
                'impressions': int(insight_data.get('impressions', 0)),
                'clicks': int(insight_data.get('clicks', 0)),
                'spend': float(insight_data.get('spend', 0)),
                'reach': int(insight_data.get('reach', 0)),
                'frequency': float(insight_data.get('frequency', 0)),
                'ctr': float(insight_data.get('ctr', 0)),
                'cpc': float(insight_data.get('cpc', 0)),
                'cpm': float(insight_data.get('cpm', 0)),
                'purchases': purchases,
                'cpa': cpa,
                'roas': None,  # Calculate if revenue available
                'date_range': {
                    'date_preset': date_preset,
                    'since': date_from,
                    'until': date_until
                },
            }

            logger.info(f"Fetched insights for campaign {campaign_id}")
            return result

        except Exception as e:
            logger.error(
                f"Error fetching insights for campaign {campaign_id}: {e}")
            return None

    async def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """
        Process natural language query

        Args:
            query: User query in Portuguese

        Returns:
            Structured response with type and data
        """
        query_lower = query.lower()

        # Simple pattern matching (TODO: Replace with LangChain in future)
        if any(word in query_lower for word in ['listar', 'mostrar', 'campanhas']):
            campaigns = await self.get_campaigns(status_filter="ACTIVE")
            return {
                'type': 'campaigns_list',
                'query': query,
                'data': campaigns
            }

        elif any(word in query_lower for word in ['performance', 'desempenho']):
            campaigns = await self.get_campaigns(status_filter="ACTIVE")
            campaigns_with_insights = []

            for campaign in campaigns[:10]:  # Limit to 10 for performance
                insights = await self.get_campaign_insights(campaign['id'])
                if insights:
                    campaigns_with_insights.append({
                        **campaign,
                        'insights': insights
                    })

            return {
                'type': 'performance_analysis',
                'query': query,
                'data': campaigns_with_insights
            }

        elif any(word in query_lower for word in ['gasto', 'gastei', 'spend']):
            campaigns = await self.get_campaigns(status_filter="ACTIVE")
            total_spend = 0.0

            for campaign in campaigns:
                insights = await self.get_campaign_insights(campaign['id'], 'today')
                if insights:
                    total_spend += insights['spend']

            return {
                'type': 'spend_analysis',
                'query': query,
                'data': {
                    'total_spend': total_spend,
                    'campaigns_count': len(campaigns),
                    'date': 'today'
                }
            }

        else:
            # Unknown command
            return {
                'type': 'general_info',
                'query': query,
                'data': {
                    'message': 'Comando não reconhecido. Tente: "Liste campanhas ativas", "Como está a performance?", "Quanto gastei hoje?"',
                    'available_commands': [
                        'Listar campanhas ativas',
                        'Mostrar performance',
                        'Quanto gastei hoje?',
                        'Quais campanhas têm CTR baixo?'
                    ]
                }
            }
