"""
Campaign Optimizer
Otimização inteligente de campanhas (apenas sugestões, sem ações automáticas)
"""
from typing import List, Dict, Any
from decimal import Decimal
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CampaignOptimizer:
    """
    Otimizador de campanhas

    IMPORTANTE: Apenas gera sugestões, não executa ações automaticamente
    """

    def __init__(
        self,
        ctr_threshold: float = 1.0,
        cpa_threshold: float = 50.0,
        budget_adjustment_pct: float = 0.20
    ):
        """
        Initialize optimizer

        Args:
            ctr_threshold: Minimum acceptable CTR (%)
            cpa_threshold: Maximum acceptable CPA (R$)
            budget_adjustment_pct: Max budget adjustment (0.20 = ±20%)
        """
        self.ctr_threshold = ctr_threshold
        self.cpa_threshold = cpa_threshold
        self.budget_adjustment_pct = budget_adjustment_pct

    def evaluate_campaigns(
        self,
        campaigns_with_insights: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict]]:
        """
        Evaluate all campaigns and categorize by performance

        Args:
            campaigns_with_insights: List of campaigns with insights data

        Returns:
            Dictionary with categorized campaigns
        """
        underperforming = []
        good_performers = []
        excellent_performers = []

        for campaign in campaigns_with_insights:
            insights = campaign.get('insights', {})
            ctr = insights.get('ctr', 0)
            cpa = insights.get('cpa')

            # Categorize
            is_underperforming = False
            reasons = []

            if ctr < self.ctr_threshold:
                is_underperforming = True
                reasons.append(
                    f"CTR baixo: {ctr:.2f}% (mínimo: {self.ctr_threshold}%)")

            if cpa and cpa > self.cpa_threshold:
                is_underperforming = True
                reasons.append(
                    f"CPA alto: R${cpa:.2f} (máximo: R${self.cpa_threshold})")

            if is_underperforming:
                underperforming.append({
                    **campaign,
                    'reasons': reasons
                })
            elif ctr >= self.ctr_threshold * 1.5:  # 50% above threshold
                excellent_performers.append(campaign)
            else:
                good_performers.append(campaign)

        return {
            'underperforming': underperforming,
            'good': good_performers,
            'excellent': excellent_performers
        }

    def generate_pause_suggestions(
        self,
        underperforming_campaigns: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Generate pause suggestions for underperforming campaigns

        Args:
            underperforming_campaigns: Campaigns with poor performance

        Returns:
            List of pause suggestions
        """
        suggestions = []

        for campaign in underperforming_campaigns:
            suggestion = {
                'campaign_id': campaign['id'],
                'campaign_name': campaign['name'],
                'type': 'PAUSE',
                'reason': '; '.join(campaign.get('reasons', [])),
                'current_status': campaign.get('status'),
                'data': {
                    'current_ctr': campaign.get('insights', {}).get('ctr'),
                    'current_cpa': campaign.get('insights', {}).get('cpa'),
                    'threshold_ctr': self.ctr_threshold,
                    'threshold_cpa': self.cpa_threshold,
                }
            }
            suggestions.append(suggestion)

        logger.info(f"Generated {len(suggestions)} pause suggestions")
        return suggestions

    def generate_budget_suggestions(
        self,
        campaigns: Dict[str, List[Dict]]
    ) -> List[Dict[str, Any]]:
        """
        Generate budget adjustment suggestions

        Args:
            campaigns: Categorized campaigns (excellent, good, underperforming)

        Returns:
            List of budget suggestions
        """
        suggestions = []

        # Increase budget for excellent performers
        for campaign in campaigns.get('excellent', []):
            current_budget = campaign.get('daily_budget')
            if current_budget:
                current_budget = float(current_budget)
                new_budget = current_budget * (1 + self.budget_adjustment_pct)

                suggestion = {
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign['name'],
                    'type': 'BUDGET_UP',
                    'reason': f"Excelente performance - CTR: {campaign.get('insights', {}).get('ctr', 0):.2f}%",
                    'data': {
                        'current_budget': current_budget,
                        'suggested_budget': round(new_budget, 2),
                        'increase_pct': self.budget_adjustment_pct * 100
                    }
                }
                suggestions.append(suggestion)

        # Decrease budget for underperformers (before pause)
        for campaign in campaigns.get('underperforming', [])[:5]:  # Limit to top 5
            current_budget = campaign.get('daily_budget')
            if current_budget:
                current_budget = float(current_budget)
                new_budget = current_budget * (1 - self.budget_adjustment_pct)

                suggestion = {
                    'campaign_id': campaign['id'],
                    'campaign_name': campaign['name'],
                    'type': 'BUDGET_DOWN',
                    'reason': '; '.join(campaign.get('reasons', [])),
                    'data': {
                        'current_budget': current_budget,
                        'suggested_budget': round(new_budget, 2),
                        'decrease_pct': self.budget_adjustment_pct * 100
                    }
                }
                suggestions.append(suggestion)

        logger.info(f"Generated {len(suggestions)} budget suggestions")
        return suggestions

    def generate_reallocation_plan(
        self,
        campaigns: Dict[str, List[Dict]]
    ) -> Dict[str, Any]:
        """
        Generate intelligent budget reallocation plan

        Args:
            campaigns: Categorized campaigns

        Returns:
            Reallocation plan with from/to campaigns
        """
        underperforming = campaigns.get('underperforming', [])
        excellent = campaigns.get('excellent', [])

        if not underperforming or not excellent:
            return {'reallocations': []}

        # Calculate total budget to reallocate
        total_to_reallocate = 0.0
        for campaign in underperforming:
            budget = campaign.get('daily_budget')
            if budget:
                # Realocate 50% of underperforming
                total_to_reallocate += float(budget) * 0.5

        # Distribute to excellent performers
        reallocations = []
        budget_per_excellent = total_to_reallocate / len(excellent)

        for campaign in excellent:
            reallocation = {
                'to_campaign_id': campaign['id'],
                'to_campaign_name': campaign['name'],
                'additional_budget': round(budget_per_excellent, 2),
                'reason': f"Realocação de campanhas com baixa performance"
            }
            reallocations.append(reallocation)

        plan = {
            'total_reallocated': round(total_to_reallocate, 2),
            'from_campaigns_count': len(underperforming),
            'to_campaigns_count': len(excellent),
            'reallocations': reallocations
        }

        logger.info(
            f"Generated reallocation plan: R${total_to_reallocate:.2f}")
        return plan
