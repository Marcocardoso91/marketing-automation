"""
Notion Client
Integração com Notion para documentação e relatórios
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

import httpx

from src.utils.config import settings
from src.utils.exceptions import NotionAPIError
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

NOTION_API_BASE_URL = "https://api.notion.com/v1"
NOTION_DEFAULT_VERSION = "2022-06-28"


class NotionClient:
    """
    Cliente para integração com Notion via REST API.

    Quando o token ou o database não estiverem configurados os métodos lançam
    `NotionAPIError`. Desta forma a camada FastAPI pode responder com um
    HTTP 503 ao invés de retornar sucesso com `None`.
    """

    def __init__(self, database_id: Optional[str] = None):
        self.database_id = database_id or settings.NOTION_DATABASE_ID
        self.token = settings.NOTION_API_TOKEN or os.getenv("NOTION_TOKEN")
        self.timeout = float(os.getenv("NOTION_TIMEOUT", "30"))

        if not self.token:
            logger.warning(
                "NOTION_API_TOKEN not configured – Notion endpoints will return 503"
            )

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _ensure_configured(
        self,
        database_id: Optional[str] = None,
        *,
        require_database: bool = False,
    ) -> str:
        if not self.token:
            raise NotionAPIError(
                message="Notion API token is not configured; set NOTION_API_TOKEN"
            )

        resolved_database = database_id or self.database_id
        if require_database and not resolved_database:
            raise NotionAPIError(
                message="Notion database_id not provided; configure NOTION_DATABASE_ID"
            )
        return resolved_database

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_DEFAULT_VERSION,
            "Content-Type": "application/json",
        }

    async def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{NOTION_API_BASE_URL}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    headers=self._headers(),
                    json=payload,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Notion API error (%s): %s",
                exc.response.status_code,
                exc.response.text,
            )
            raise NotionAPIError(
                message=f"Notion API error ({exc.response.status_code})",
                details={"status": exc.response.status_code},
            ) from exc
        except httpx.RequestError as exc:
            logger.error("Unable to reach Notion API: %s", exc)
            raise NotionAPIError(
                message="Unable to reach Notion API", details={"error": str(exc)}
            ) from exc

    async def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{NOTION_API_BASE_URL}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self._headers(),
                    json=payload,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "Notion API error (%s): %s",
                exc.response.status_code,
                exc.response.text,
            )
            raise NotionAPIError(
                message=f"Notion API error ({exc.response.status_code})",
                details={"status": exc.response.status_code},
            ) from exc
        except httpx.RequestError as exc:
            logger.error("Unable to reach Notion API: %s", exc)
            raise NotionAPIError(
                message="Unable to reach Notion API", details={"error": str(exc)}
            ) from exc

    @staticmethod
    def _title_property(title: str) -> Dict[str, Any]:
        return {
            "Name": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": title},
                    }
                ]
            }
        }

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    async def create_campaign_report(
        self,
        campaign_data: Dict[str, Any],
        insights: Dict[str, Any],
        score: float,
        suggestions: List[Dict[str, Any]],
        *,
        database_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Cria relatório de campanha no Notion e retorna a URL da página.
        """
        resolved_database = self._ensure_configured(
            database_id, require_database=True
        )

        title = f"📊 {campaign_data['name']} - {datetime.now().strftime('%d/%m/%Y')}"
        content_blocks = self._format_campaign_report(
            campaign_data, insights, score, suggestions
        )

        payload = {
            "parent": {"database_id": resolved_database},
            "properties": self._title_property(title),
            "children": content_blocks,
        }

        response = await self._post("/pages", payload)
        page_url = response.get("url")
        logger.info("Created Notion campaign report: %s", page_url)
        return page_url

    async def create_daily_summary(
        self,
        date: str,
        total_spend: float,
        campaigns_analyzed: int,
        top_performers: List[Dict],
        underperformers: List[Dict],
        *,
        database_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Cria sumário diário no Notion e retorna a URL da página.
        """
        resolved_database = self._ensure_configured(
            database_id, require_database=True
        )

        title = f"📅 Relatório Diário - {date}"
        content_blocks = self._format_daily_summary(
            date,
            total_spend,
            campaigns_analyzed,
            top_performers,
            underperformers,
        )

        payload = {
            "parent": {"database_id": resolved_database},
            "properties": self._title_property(title),
            "children": content_blocks,
        }

        response = await self._post("/pages", payload)
        page_url = response.get("url")
        logger.info("Created Notion daily summary: %s", page_url)
        return page_url

    async def save_suggestion(
        self,
        suggestion: Dict[str, Any],
        *,
        database_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Salva sugestão de otimização no Notion e retorna a URL da página.
        """
        resolved_database = self._ensure_configured(
            database_id, require_database=True
        )

        title = f"💡 {suggestion['campaign_name']} - {suggestion['type']}"
        content_blocks = self._format_suggestion(suggestion)

        payload = {
            "parent": {"database_id": resolved_database},
            "properties": self._title_property(title),
            "children": content_blocks,
        }

        response = await self._post("/pages", payload)
        page_url = response.get("url")
        logger.info("Created Notion suggestion page: %s", page_url)
        return page_url

    async def search_pages(
        self,
        query: str,
        filter_database: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search Notion pages using Notion API.
        """
        self._ensure_configured()

        payload: Dict[str, Any] = {
            "query": query,
            "sort": {
                "direction": "descending",
                "timestamp": "last_edited_time",
            },
        }

        if filter_database or self.database_id:
            payload["filter"] = {
                "property": "object",
                "value": "page",
            }

        response = await self._request("POST", "/search", payload)
        results = response.get("results", [])

        formatted_results: List[Dict[str, Any]] = []
        for page in results:
            title = "Untitled"
            properties = page.get("properties", {})
            for prop_data in properties.values():
                if prop_data.get("type") == "title":
                    title_array = prop_data.get("title", [])
                    if title_array:
                        title = title_array[0].get("plain_text", "Untitled")
                    break

            formatted_results.append(
                {
                    "id": page.get("id"),
                    "title": title,
                    "url": page.get("url"),
                    "last_edited_time": page.get("last_edited_time"),
                    "created_time": page.get("created_time"),
                    "object": page.get("object", "page"),
                }
            )

        logger.info("Found %d results for Notion query '%s'", len(formatted_results), query)
        return formatted_results

    # ------------------------------------------------------------------ #
    # Content helpers
    # ------------------------------------------------------------------ #
    def _format_campaign_report(
        self,
        campaign: Dict[str, Any],
        insights: Dict[str, Any],
        score: float,
        suggestions: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        rating = (
            "🟢 Excelente"
            if score >= 80
            else "🟡 Bom"
            if score >= 60
            else "🟠 Regular"
            if score >= 40
            else "🔴 Ruim"
        )

        blocks: List[Dict[str, Any]] = [
            self._paragraph_block(
                f"Score geral: {score:.1f}/100 – {rating}"
            ),
            self._heading_block("Métricas Principais"),
            self._bulleted_block(
                [
                    f"CTR: {insights.get('ctr', 0):.2f}%",
                    f"CPC: R$ {insights.get('cpc', 0):.2f}",
                    f"CPM: R$ {insights.get('cpm', 0):.2f}",
                    f"CPA: R$ {insights.get('cpa', 0):.2f}",
                    f"ROAS: {insights.get('roas', 'N/A')}",
                ]
            ),
            self._heading_block("Gastos"),
            self._bulleted_block(
                [
                    f"Spend Total: R$ {insights.get('spend', 0):,.2f}",
                    f"Orçamento Diário: R$ {campaign.get('daily_budget', 'N/A')}",
                ]
            ),
            self._heading_block("Engajamento"),
            self._bulleted_block(
                [
                    f"Impressões: {insights.get('impressions', 0):,}",
                    f"Cliques: {insights.get('clicks', 0):,}",
                    f"Alcance: {insights.get('reach', 0):,}",
                    f"Frequência: {insights.get('frequency', 0):.2f}",
                ]
            ),
        ]

        if suggestions:
            suggestion_lines = [
                f"{idx+1}. {item['type']} – {item['reason']}"
                for idx, item in enumerate(suggestions)
            ]
            blocks.append(self._heading_block("Sugestões"))
            blocks.append(self._bulleted_block(suggestion_lines))

        blocks.append(
            self._paragraph_block(
                f"Geração: {datetime.now().strftime('%d/%m/%Y %H:%M')} – Sistema: Facebook Ads AI Agent"
            )
        )
        return blocks

    def _format_daily_summary(
        self,
        date: str,
        total_spend: float,
        campaigns_analyzed: int,
        top_performers: List[Dict],
        underperformers: List[Dict],
    ) -> List[Dict[str, Any]]:
        blocks: List[Dict[str, Any]] = [
            self._paragraph_block(f"Data do relatório: {date}"),
            self._heading_block("Resumo Financeiro"),
            self._bulleted_block(
                [
                    f"Gasto total: R$ {total_spend:,.2f}",
                    f"Campanhas analisadas: {campaigns_analyzed}",
                ]
            ),
        ]

        if top_performers:
            lines = []
            for idx, campaign in enumerate(top_performers[:5], 1):
                insights = campaign.get("insights", {})
                lines.append(
                    f"{idx}. {campaign['name']} – Score {campaign.get('score', 0):.1f}/100 | CTR {insights.get('ctr', 0):.2f}% | Spend R$ {insights.get('spend', 0):.2f}"
                )
            blocks.append(self._heading_block("Top Performers"))
            blocks.append(self._bulleted_block(lines))

        if underperformers:
            lines = []
            for idx, campaign in enumerate(underperformers[:5], 1):
                insights = campaign.get("insights", {})
                lines.append(
                    f"{idx}. {campaign['name']} – Problemas: {', '.join(campaign.get('reasons', [])) or 'N/A'} | CTR {insights.get('ctr', 0):.2f}% | Spend R$ {insights.get('spend', 0):.2f}"
                )
            blocks.append(self._heading_block("Campanhas com Atenção"))
            blocks.append(self._bulleted_block(lines))

        return blocks

    def _format_suggestion(self, suggestion: Dict[str, Any]) -> List[Dict[str, Any]]:
        data_lines = [
            f"{key}: {value}" for key, value in suggestion.get("data", {}).items()
        ]
        blocks = [
            self._paragraph_block(
                f"Campanha: {suggestion['campaign_name']} ({suggestion['campaign_id']})"
            ),
            self._paragraph_block(f"Tipo: {suggestion['type']}"),
            self._paragraph_block(f"Motivo: {suggestion['reason']}"),
        ]
        if data_lines:
            blocks.append(self._heading_block("Dados"))
            blocks.append(self._bulleted_block(data_lines))
        return blocks

    @staticmethod
    def _paragraph_block(text: str) -> Dict[str, Any]:
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text},
                    }
                ]
            },
        }

    @staticmethod
    def _heading_block(text: str) -> Dict[str, Any]:
        return {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text},
                    }
                ]
            },
        }

    @staticmethod
    def _bulleted_block(lines: List[str]) -> Dict[str, Any]:
        bullet_text = "\n".join(f"• {line}" for line in lines)
        return NotionClient._paragraph_block(bullet_text)


# Singleton
_notion_client: Optional[NotionClient] = None


def get_notion_client(database_id: Optional[str] = None) -> NotionClient:
    """Get singleton Notion client"""
    global _notion_client
    if _notion_client is None:
        _notion_client = NotionClient(database_id)
    elif database_id:
        _notion_client.database_id = database_id
    return _notion_client
