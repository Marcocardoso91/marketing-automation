#!/usr/bin/env python3
"""
TikTok Metrics Collector
Coleta métricas do TikTok via Marketing API ou Display API
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class TikTokCollector:
    """Coletor de métricas do TikTok"""

    def __init__(self):
        # TikTok Marketing API (para quem usa TikTok Ads)
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        self.advertiser_id = os.getenv("TIKTOK_ADVERTISER_ID")

        # TikTok Display API (para métricas orgânicas)
        self.client_key = os.getenv("TIKTOK_CLIENT_KEY")
        self.client_secret = os.getenv("TIKTOK_CLIENT_SECRET")
        self.username = os.getenv("TIKTOK_USERNAME")

        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"
        self.display_url = "https://open.tiktokapis.com/v2"

    def get_ad_metrics(self, date_from: str, date_until: str) -> Optional[Dict[str, Any]]:
        """
        Buscar métricas de TikTok Ads (Marketing API)
        Requer conta de anúncios ativa
        """
        if not self.access_token or not self.advertiser_id:
            print("⚠️  TikTok Ads: Credenciais não configuradas")
            return None

        print("🔄 Buscando métricas TikTok Ads...")

        url = f"{self.base_url}/reports/integrated/get/"
        headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

        payload = {
            "advertiser_id": self.advertiser_id,
            "report_type": "BASIC",
            "data_level": "AUCTION_ADVERTISER",
            "dimensions": ["advertiser_id"],
            "metrics": [
                "spend",
                "impressions",
                "clicks",
                "reach",
                "ctr",
                "cpc",
                "cost_per_1000_reached"
            ],
            "start_date": date_from,
            "end_date": date_until,
            "page_size": 1000
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()

                if data.get("code") == 0 and data.get("data"):
                    metrics = data["data"]["list"][0] if data["data"].get("list") else {}

                    result = {
                        "spend": float(metrics.get("spend", 0)),
                        "impressions": int(metrics.get("impressions", 0)),
                        "clicks": int(metrics.get("clicks", 0)),
                        "reach": int(metrics.get("reach", 0)),
                        "ctr": float(metrics.get("ctr", 0)),
                        "cpc": float(metrics.get("cpc", 0)),
                        "cpm": float(metrics.get("cost_per_1000_reached", 0)),
                        "raw_data": metrics
                    }

                    print(f"✅ TikTok Ads: {result['impressions']} impressões, R$ {result['spend']:.2f} gastos")
                    return result
                else:
                    print(f"❌ TikTok Ads Error: {data.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"❌ TikTok Ads HTTP Error: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ TikTok Ads Exception: {str(e)}")
            return None

    def get_organic_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Buscar métricas orgânicas do TikTok (Display API)
        Requer aprovação da Display API
        """
        if not self.client_key or not self.client_secret:
            print("⚠️  TikTok Orgânico: Display API não configurada")
            return None

        print("🔄 Buscando métricas orgânicas TikTok...")

        # Nota: Display API requer OAuth 2.0 flow complexo
        # Para simplificar, retornar None e recomendar n8n
        print("💡 Recomendação: Use n8n workflow para TikTok orgânico")
        print("   A Display API requer OAuth 2.0 que é complexo de implementar")
        return None

    def process_metrics(self, ad_metrics: Optional[Dict], organic_metrics: Optional[Dict]) -> Optional[Dict[str, Any]]:
        """Processar e consolidar métricas do TikTok"""
        if not ad_metrics and not organic_metrics:
            return None

        yesterday = datetime.now() - timedelta(days=1)

        # Consolidar métricas (priorizar ads, fallback para orgânico)
        metrics = ad_metrics or organic_metrics or {}

        return {
            "data": yesterday.strftime("%Y-%m-%d"),
            "source": "tiktok",
            "spend": round(metrics.get("spend", 0), 2),
            "reach": metrics.get("reach", 0),
            "impressions": metrics.get("impressions", 0),
            "clicks": metrics.get("clicks", 0),
            "ctr": round(metrics.get("ctr", 0), 2),
            "cpc": round(metrics.get("cpc", 0), 4),
            "cpm": round(metrics.get("cpm", 0), 2),
            "conversions": 0,  # TikTok não retorna diretamente
            "new_followers": 0,  # Precisa de endpoint separado
            "notes": f"TikTok: {metrics.get('impressions', 0)} impressões",
            "raw_data": metrics
        }


def get_tiktok_metrics(date_from: str = None, date_until: str = None) -> Optional[Dict[str, Any]]:
    """
    Função helper para buscar métricas do TikTok

    Args:
        date_from: Data inicial (YYYY-MM-DD), default: ontem
        date_until: Data final (YYYY-MM-DD), default: ontem

    Returns:
        Dicionário com métricas processadas ou None
    """
    if not date_from:
        yesterday = datetime.now() - timedelta(days=1)
        date_from = yesterday.strftime("%Y-%m-%d")
        date_until = date_from

    collector = TikTokCollector()

    # Tentar TikTok Ads primeiro
    ad_metrics = collector.get_ad_metrics(date_from, date_until)

    # Se não tiver ads, tentar orgânico
    organic_metrics = None
    if not ad_metrics:
        organic_metrics = collector.get_organic_metrics()

    return collector.process_metrics(ad_metrics, organic_metrics)
