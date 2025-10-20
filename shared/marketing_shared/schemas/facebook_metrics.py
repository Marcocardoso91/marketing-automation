"""
Schemas Pydantic para métricas do Facebook Ads.
Compartilhado entre API e Analytics.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date as Date, datetime as DateTime
from typing import Optional, List


class CampaignMetricSchema(BaseModel):
    """Schema padronizado para métricas de campanha Meta Ads"""

    campaign_id: str = Field(...,
                             description="ID único da campanha", min_length=1)
    campaign_name: str = Field(...,
                               description="Nome da campanha", min_length=1)
    date: Date = Field(..., description="Data das métricas")

    # Métricas principais
    impressions: int = Field(ge=0, description="Número de impressões")
    clicks: int = Field(ge=0, description="Número de cliques")
    spend: float = Field(ge=0, description="Valor gasto em reais")
    reach: int = Field(ge=0, description="Alcance único")
    frequency: float = Field(ge=0, description="Frequência média")

    # Métricas calculadas
    ctr: float = Field(ge=0, le=100, description="Click-through rate (%)")
    cpc: float = Field(ge=0, description="Cost per click (R$)")
    cpe: Optional[float] = Field(
        None, ge=0, description="Cost per engagement (R$)")
    cpm: Optional[float] = Field(None, ge=0, description="Cost per mille (R$)")

    # Conversões
    conversions: int = Field(ge=0, description="Número de conversões")
    conversion_rate: Optional[float] = Field(
        None, ge=0, le=100, description="Taxa de conversão (%)")
    roas: Optional[float] = Field(None, description="Return on ad spend")

    @field_validator('date')
    @classmethod
    def validate_date_not_future(cls, v: Date) -> Date:
        """Valida que data não está no futuro"""
        if v > Date.today():
            raise ValueError('Data não pode estar no futuro')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "campaign_id": "123456789",
                "campaign_name": "Campanha Teste Q4",
                "date": "2025-10-18",
                "impressions": 10000,
                "clicks": 500,
                "spend": "250.00",
                "reach": 8000,
                "frequency": "1.25",
                "ctr": "5.0",
                "cpc": "0.50",
                "cpe": "0.35",
                "cpm": "25.00",
                "conversions": 50,
                "conversion_rate": "10.0",
                "roas": "4.5"
            }
        }


class ExportedMetricsResponse(BaseModel):
    """Response do endpoint de exportação"""

    campaigns: List[CampaignMetricSchema]
    total_campaigns: int = Field(ge=0)
    date_from: Date
    date_until: Date
    exported_at: DateTime
    data_source: str = Field(default="facebook-ads-ai-agent")
    version: str = Field(default="1.0.0")

    @field_validator('total_campaigns')
    @classmethod
    def validate_total_matches_list(cls, v: int, info) -> int:
        """Valida que total_campaigns corresponde ao tamanho da lista"""
        campaigns = info.data.get('campaigns', [])
        if v != len(campaigns):
            raise ValueError(
                f'total_campaigns ({v}) não corresponde ao tamanho da lista ({len(campaigns)})')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "campaigns": [],
                "total_campaigns": 0,
                "date_from": "2025-10-18",
                "date_until": "2025-10-18",
                "exported_at": "2025-10-18T10:30:00Z",
                "data_source": "facebook-ads-ai-agent",
                "version": "1.0.0"
            }
        }
