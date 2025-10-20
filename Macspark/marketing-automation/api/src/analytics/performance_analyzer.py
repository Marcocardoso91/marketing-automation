"""
Performance Analyzer
Análise de performance de campanhas com ML
"""
from typing import List, Dict, Any, Optional
from decimal import Decimal
import statistics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PerformanceAnalyzer:
    """
    Analisa performance de campanhas

    Features:
    - Scoring 0-100
    - Anomaly detection
    - Trend analysis
    """

    def __init__(self):
        """Initialize analyzer"""
        # Thresholds baseados em benchmarks do mercado
        self.ctr_benchmark = 2.0  # 2% CTR médio
        self.cpa_benchmark = 50.0  # R$50 CPA médio
        self.roas_benchmark = 2.5  # 2.5x ROAS mínimo

    def calculate_score(self, insight: Dict[str, Any]) -> float:
        """
        Calculate performance score (0-100)

        Args:
            insight: Campaign insight data

        Returns:
            Score between 0 and 100
        """
        try:
            score = 0.0
            weights = []

            # CTR score (weight: 30%)
            ctr = float(insight.get('ctr', 0))
            if ctr > 0:
                ctr_score = min((ctr / self.ctr_benchmark) * 100, 100)
                score += ctr_score * 0.3
                weights.append(0.3)

            # CPA score (weight: 40%)
            cpa = insight.get('cpa')
            if cpa and float(cpa) > 0:
                # Lower CPA is better, so invert the score
                cpa_score = max(
                    100 - ((float(cpa) / self.cpa_benchmark) * 100), 0)
                score += cpa_score * 0.4
                weights.append(0.4)

            # ROAS score (weight: 30%)
            roas = insight.get('roas')
            if roas and float(roas) > 0:
                roas_score = min(
                    (float(roas) / self.roas_benchmark) * 100, 100)
                score += roas_score * 0.3
                weights.append(0.3)

            # Normalize by actual weights used
            if weights:
                score = score / sum(weights)

            return round(score, 2)

        except Exception as e:
            logger.error(f"Error calculating score: {e}")
            return 0.0

    def detect_anomalies(
        self,
        current_insight: Dict[str, Any],
        historical_insights: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Detect anomalies comparing current with historical data

        Args:
            current_insight: Latest insight
            historical_insights: Past insights (7-30 days)

        Returns:
            List of detected anomalies
        """
        anomalies = []

        if not historical_insights or len(historical_insights) < 3:
            return anomalies

        try:
            # Analyze CTR
            historical_ctr = [float(i.get('ctr', 0))
                              for i in historical_insights if i.get('ctr')]
            if historical_ctr:
                mean_ctr = statistics.mean(historical_ctr)
                std_ctr = statistics.stdev(historical_ctr) if len(
                    historical_ctr) > 1 else 0
                current_ctr = float(current_insight.get('ctr', 0))

                if current_ctr < (mean_ctr - 2 * std_ctr):
                    anomalies.append(
                        f"CTR anormalmente baixo: {current_ctr:.2f}% (média: {mean_ctr:.2f}%)")

            # Analyze spend
            historical_spend = [float(i.get('spend', 0))
                                for i in historical_insights if i.get('spend')]
            if historical_spend:
                mean_spend = statistics.mean(historical_spend)
                std_spend = statistics.stdev(historical_spend) if len(
                    historical_spend) > 1 else 0
                current_spend = float(current_insight.get('spend', 0))

                if current_spend > (mean_spend + 2 * std_spend):
                    anomalies.append(
                        f"Gasto anormalmente alto: R${current_spend:.2f} (média: R${mean_spend:.2f})")

            # Analyze CPA if available
            historical_cpa = [float(i.get('cpa', 0)) for i in historical_insights if i.get(
                'cpa') and float(i.get('cpa', 0)) > 0]
            if historical_cpa and current_insight.get('cpa'):
                mean_cpa = statistics.mean(historical_cpa)
                std_cpa = statistics.stdev(historical_cpa) if len(
                    historical_cpa) > 1 else 0
                current_cpa = float(current_insight.get('cpa', 0))

                if current_cpa > (mean_cpa + 2 * std_cpa):
                    anomalies.append(
                        f"CPA anormalmente alto: R${current_cpa:.2f} (média: R${mean_cpa:.2f})")

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")

        return anomalies

    def analyze_trends(
        self,
        insights_7d: List[Dict],
        insights_14d: List[Dict],
        insights_30d: List[Dict]
    ) -> Dict[str, Any]:
        """
        Analyze performance trends over different periods

        Args:
            insights_7d: Last 7 days insights
            insights_14d: Last 14 days insights
            insights_30d: Last 30 days insights

        Returns:
            Trend analysis with growth rates
        """
        try:
            def calc_avg(insights: List[Dict], metric: str) -> float:
                values = [float(i.get(metric, 0))
                          for i in insights if i.get(metric)]
                return statistics.mean(values) if values else 0.0

            trends = {
                'ctr': {
                    '7d': calc_avg(insights_7d, 'ctr'),
                    '14d': calc_avg(insights_14d, 'ctr'),
                    '30d': calc_avg(insights_30d, 'ctr'),
                },
                'cpa': {
                    '7d': calc_avg(insights_7d, 'cpa'),
                    '14d': calc_avg(insights_14d, 'cpa'),
                    '30d': calc_avg(insights_30d, 'cpa'),
                },
                'spend': {
                    '7d': calc_avg(insights_7d, 'spend'),
                    '14d': calc_avg(insights_14d, 'spend'),
                    '30d': calc_avg(insights_30d, 'spend'),
                },
            }

            # Calculate growth rates
            for metric in ['ctr', 'cpa', 'spend']:
                val_7d = trends[metric]['7d']
                val_30d = trends[metric]['30d']

                if val_30d > 0:
                    growth = ((val_7d - val_30d) / val_30d) * 100
                    trends[metric]['growth_rate'] = round(growth, 2)
                else:
                    trends[metric]['growth_rate'] = 0.0

            return trends

        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            return {}
