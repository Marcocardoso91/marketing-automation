#!/usr/bin/env python3
"""
Script para buscar métricas do Meta Ads e adicionar no Notion
Backup manual caso o N8n falhe
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# URLs das APIs
META_API_URL = "https://graph.facebook.com/v21.0"
NOTION_API_URL = "https://api.notion.com/v1"


def get_meta_ads_metrics(date_preset: str = "yesterday") -> Optional[List[Dict[str, Any]]]:
    """
    Busca métricas do Meta Ads API
    """
    url = f"{META_API_URL}/{META_AD_ACCOUNT_ID}/insights"

    params = {
        "access_token": META_ACCESS_TOKEN,
        "fields": ",".join(
            [
                "campaign_name",
                "spend",
                "impressions",
                "reach",
                "clicks",
                "ctr",
                "cpc",
                "cpp",
                "frequency",
                "actions",
            ]
        ),
        "date_preset": date_preset,
        "level": "campaign",
        "time_increment": 1,
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Erro ao buscar dados do Meta: {response.status_code}")
        print(response.text)
        return None

    data = response.json().get("data", [])
    return data if isinstance(data, list) else []


def process_metrics(campaigns_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Processa dados das campanhas e agrega métricas
    """
    if not campaigns_data:
        print("⚠️ Nenhum dado encontrado")
        return None

    # Agregar métricas de todas campanhas
    total_spend: float = 0.0
    total_impressions: int = 0
    total_reach: int = 0
    total_clicks: int = 0
    total_frequency: float = 0.0
    total_followers: int = 0
    campaign_count = len(campaigns_data)

    for campaign in campaigns_data:
        total_spend += float(campaign.get("spend", 0))
        total_impressions += int(campaign.get("impressions", 0))
        total_reach += int(campaign.get("reach", 0))
        total_clicks += int(campaign.get("clicks", 0))
        total_frequency += float(campaign.get("frequency", 0))

        # Buscar ações de follow/save
        actions = campaign.get("actions", [])
        for action in actions:
            if action.get("action_type") in ["follow", "onsite_conversion.post_save"]:
                total_followers += int(action.get("value", 0))

    # Calcular métricas derivadas
    avg_ctr = (total_clicks / total_impressions) if total_impressions > 0 else 0
    avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    avg_cpe = (total_spend / total_followers) if total_followers > 0 else 0
    avg_frequency = (total_frequency /
                     campaign_count) if campaign_count > 0 else 0
    cost_per_follower = (
        total_spend / total_followers) if total_followers > 0 else 0

    return {
        "data": datetime.now().strftime("%Y-%m-%d"),
        "gasto_ads": total_spend,
        "alcance": total_reach,
        "ctr": avg_ctr,
        "cpc": avg_cpc,
        "cpe": avg_cpe,
        "frequencia": avg_frequency,
        "novos_seguidores": total_followers,
        "custo_por_seguidor": cost_per_follower,
        "notas": f"Dados coletados via script Python - {campaign_count} campanhas",
    }


def add_to_notion(metrics: Dict[str, Any]) -> bool:
    """
    Adiciona registro no database do Notion
    """
    url = f"{NOTION_API_URL}/pages"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # Mapear nomes dos campos (ajustar conforme seu database)
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Data": {"title": [{"text": {"content": metrics["data"]}}]},
            "Gasto Ads (R$)": {"number": metrics["gasto_ads"]},
            "Alcance": {"number": metrics["alcance"]},
            "CTR (%)": {"number": metrics["ctr"]},
            "CPC (R$)": {"number": metrics["cpc"]},
            "CPE (R$)": {"number": metrics["cpe"]},
            "Frequência": {"number": metrics["frequencia"]},
            "Novos Seguidores": {"number": metrics["novos_seguidores"]},
            "Custo por Seguidor": {"number": metrics["custo_por_seguidor"]},
            "Notas": {"rich_text": [{"text": {"content": metrics["notas"]}}]},
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"✅ Métricas adicionadas no Notion com sucesso!")
        return True
    else:
        print(f"❌ Erro ao adicionar no Notion: {response.status_code}")
        print(response.text)
        return False


def main() -> None:
    """
    Função principal
    """
    print("🚀 Iniciando coleta de métricas...")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. Buscar dados do Meta Ads
    print("📊 Buscando dados do Meta Ads...")
    campaigns_data = get_meta_ads_metrics()

    if not campaigns_data:
        print("❌ Falha ao buscar dados. Encerrando.")
        return

    print(f"✅ {len(campaigns_data)} campanhas encontradas")
    print()

    # 2. Processar métricas
    print("⚙️ Processando métricas...")
    metrics = process_metrics(campaigns_data)

    if not metrics:
        print("❌ Falha ao processar dados. Encerrando.")
        return

    # Mostrar resumo
    print("📈 Resumo das métricas:")
    print(f"   Gasto: R$ {metrics['gasto_ads']:.2f}")
    print(f"   Alcance: {metrics['alcance']:,}")
    print(f"   CTR: {metrics['ctr']:.2%}")
    print(f"   CPE: R$ {metrics['cpe']:.2f}")
    print(f"   Novos Seguidores: {metrics['novos_seguidores']}")
    print(f"   Custo/Seguidor: R$ {metrics['custo_por_seguidor']:.2f}")
    print()

    # 3. Adicionar no Notion
    print("📝 Adicionando no Notion...")
    success = add_to_notion(metrics)

    if success:
        print()
        print("✅ Processo concluído com sucesso!")
        print(f"🔗 Acesse: https://www.notion.so/{NOTION_DATABASE_ID}")
    else:
        print()
        print("❌ Falha ao adicionar no Notion")


if __name__ == "__main__":
    # Verificar variáveis de ambiente
    required_vars = [
        "META_ACCESS_TOKEN",
        "META_AD_ACCOUNT_ID",
        "NOTION_TOKEN",
        "NOTION_DATABASE_ID",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print("❌ Variáveis de ambiente faltando:")
        for var in missing:
            print(f"   - {var}")
        print()
        print("💡 Copie .env.example para .env e preencha os valores")
        exit(1)

    main()
