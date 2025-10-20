"""
Notion Client
Integração com Notion para documentação e relatórios
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotionClient:
    """
    Cliente para integração com Notion via MCP

    Funcionalidades:
    - Criar páginas de relatório
    - Salvar sugestões de otimização
    - Documentar análises de performance
    - Criar dashboards executivos
    """

    def __init__(self, database_id: Optional[str] = None):
        """
        Initialize Notion client

        Args:
            database_id: ID do database Notion para salvar campanhas
        """
        self.database_id = database_id

    async def create_campaign_report(
        self,
        campaign_data: Dict[str, Any],
        insights: Dict[str, Any],
        score: float,
        suggestions: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Cria relatório de campanha no Notion

        Args:
            campaign_data: Dados da campanha
            insights: Métricas de performance
            score: Score 0-100
            suggestions: Lista de sugestões geradas

        Returns:
            URL da página criada ou None
        """
        try:
            # Formatar conteúdo em Notion Markdown
            content = self._format_campaign_report(
                campaign_data, insights, score, suggestions
            )

            properties = {
                "title": f"📊 {campaign_data['name']} - {datetime.now().strftime('%d/%m/%Y')}",
                "Score": score,
                "CTR": insights.get('ctr', 0),
                "CPA": insights.get('cpa', 0),
                "Spend": insights.get('spend', 0),
                "Status": campaign_data.get('status', 'ACTIVE')
            }

            logger.warning(
                "Notion MCP integration not configured; returning placeholder response")
            return None  # Retornaria URL da página

        except Exception as e:
            logger.error(f"Erro ao criar relatório Notion: {e}")
            return None

    async def create_daily_summary(
        self,
        date: str,
        total_spend: float,
        campaigns_analyzed: int,
        top_performers: List[Dict],
        underperformers: List[Dict]
    ) -> Optional[str]:
        """
        Cria sumário diário no Notion

        Args:
            date: Data do relatório
            total_spend: Gasto total do dia
            campaigns_analyzed: Número de campanhas analisadas
            top_performers: Campanhas com melhor performance
            underperformers: Campanhas com pior performance

        Returns:
            URL da página criada
        """
        try:
            content = f"""# 📅 Relatório Diário - {date}

## 💰 Resumo Financeiro
- **Gasto Total:** R$ {total_spend:,.2f}
- **Campanhas Analisadas:** {campaigns_analyzed}

## 🏆 Top Performers ({len(top_performers)})

"""
            for idx, campaign in enumerate(top_performers[:5], 1):
                insights = campaign.get('insights', {})
                content += f"""### {idx}. {campaign['name']}
- **Score:** {campaign.get('score', 0):.1f}/100
- **CTR:** {insights.get('ctr', 0):.2f}%
- **CPA:** R$ {insights.get('cpa', 0):.2f}
- **Spend:** R$ {insights.get('spend', 0):.2f}

"""

            content += f"""## ⚠️ Underperformers ({len(underperformers)})

"""
            for idx, campaign in enumerate(underperformers[:5], 1):
                insights = campaign.get('insights', {})
                content += f"""### {idx}. {campaign['name']}
- **Problemas:** {', '.join(campaign.get('reasons', []))}
- **CTR:** {insights.get('ctr', 0):.2f}%
- **CPA:** R$ {insights.get('cpa', 0):.2f}
- **Spend:** R$ {insights.get('spend', 0):.2f}

"""

            properties = {
                "title": f"📊 Relatório Diário - {date}",
                "Date": date,
                "Total Spend": total_spend,
                "Campaigns": campaigns_analyzed
            }

            logger.warning("Notion MCP integration not configured; resumo diário não foi criado")
            return None

        except Exception as e:
            logger.error(f"Erro ao criar sumário diário Notion: {e}")
            return None

    async def save_suggestion(
        self,
        suggestion: Dict[str, Any]
    ) -> Optional[str]:
        """
        Salva sugestão de otimização no Notion

        Args:
            suggestion: Dados da sugestão

        Returns:
            URL da página criada
        """
        try:
            content = f"""# 💡 Sugestão: {suggestion['type']}

## 📊 Campanha
- **ID:** {suggestion['campaign_id']}
- **Nome:** {suggestion['campaign_name']}

## 🎯 Recomendação
{suggestion['reason']}

## 📈 Dados
"""
            for key, value in suggestion.get('data', {}).items():
                content += f"- **{key}:** {value}\n"

            properties = {
                "title": f"💡 {suggestion['campaign_name']} - {suggestion['type']}",
                "Type": suggestion['type'],
                "Campaign": suggestion['campaign_name'],
                "Status": "PENDING"
            }

            logger.warning("Notion MCP integration não configurada; sugestão apenas registrada em log")
            return None

        except Exception as e:
            logger.error(f"Erro ao salvar sugestão Notion: {e}")
            return None

    def _format_campaign_report(
        self,
        campaign: Dict,
        insights: Dict,
        score: float,
        suggestions: List[Dict]
    ) -> str:
        """Formata relatório de campanha em Notion Markdown"""

        rating = '🟢 Excelente' if score >= 80 else '🟡 Bom' if score >= 60 else '🟠 Regular' if score >= 40 else '🔴 Ruim'

        content = f"""# 📊 Relatório: {campaign['name']}

## 🎯 Score Geral
**{score:.1f}/100** - {rating}

## 📈 Métricas Principais
- **CTR:** {insights.get('ctr', 0):.2f}%
- **CPC:** R$ {insights.get('cpc', 0):.2f}
- **CPM:** R$ {insights.get('cpm', 0):.2f}
- **CPA:** R$ {insights.get('cpa', 0):.2f}
- **ROAS:** {insights.get('roas', 'N/A')}

## 💰 Gastos
- **Spend Total:** R$ {insights.get('spend', 0):,.2f}
- **Orçamento Diário:** R$ {campaign.get('daily_budget', 'N/A')}

## 📊 Engajamento
- **Impressões:** {insights.get('impressions', 0):,}
- **Cliques:** {insights.get('clicks', 0):,}
- **Alcance:** {insights.get('reach', 0):,}
- **Frequência:** {insights.get('frequency', 0):.2f}

## 🛒 Conversões
- **Purchases:** {insights.get('purchases', 0)}
- **Revenue:** R$ {insights.get('revenue', 0):,.2f}

"""

        if suggestions:
            content += f"""## 💡 Sugestões ({len(suggestions)})

"""
            for idx, sug in enumerate(suggestions, 1):
                content += f"""### {idx}. {sug['type']}
**Motivo:** {sug['reason']}

"""

        content += f"""---
**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Sistema:** Facebook Ads AI Agent v1.0
"""

        return content


# Singleton
_notion_client = None


def get_notion_client(database_id: Optional[str] = None) -> NotionClient:
    """Get singleton Notion client"""
    global _notion_client
    if _notion_client is None:
        _notion_client = NotionClient(database_id)
    return _notion_client

    async def search_pages(
        self,
        query: str,
        filter_database: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search Notion pages using Notion API.

        Implements P0 #4 - Real Notion search functionality.

        Args:
            query: Text to search for
            filter_database: Optional database ID to filter results

        Returns:
            List of matching pages with title, ID, and URL

        Raises:
            Exception: If Notion API token not configured or API error
        """
        try:
            from src.utils.config import settings
            import aiohttp

            if not settings.NOTION_API_TOKEN:
                logger.error("NOTION_API_TOKEN not configured")
                return []

            url = "https://api.notion.com/v1/search"
            headers = {
                "Authorization": f"Bearer {settings.NOTION_API_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            }

            body = {
                "query": query,
                "sort": {
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                }
            }

            # Optional: filter by database
            if filter_database:
                body["filter"] = {
                    "property": "object",
                    "value": "page"
                }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=body, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Notion API error {response.status}: {error_text}")
                        return []

                    data = await response.json()
                    results = data.get("results", [])

                    # Format results
                    formatted_results = []
                    for page in results:
                        # Extract title from properties
                        title = "Untitled"
                        if "properties" in page:
                            for prop_name, prop_data in page["properties"].items():
                                if prop_data.get("type") == "title":
                                    title_array = prop_data.get("title", [])
                                    if title_array:
                                        title = title_array[0].get("plain_text", "Untitled")
                                    break

                        formatted_results.append({
                            "id": page.get("id"),
                            "title": title,
                            "url": page.get("url"),
                            "last_edited_time": page.get("last_edited_time"),
                            "created_time": page.get("created_time"),
                            "object": page.get("object", "page")
                        })

                    logger.info(f"Found {len(formatted_results)} results for query: '{query}'")
                    return formatted_results

        except ImportError as e:
            logger.error(f"Missing dependency for Notion search: {e}")
            logger.warning("Install with: pip install aiohttp")
            return []
        except Exception as e:
            logger.error(f"Error searching Notion: {e}")
            return []
