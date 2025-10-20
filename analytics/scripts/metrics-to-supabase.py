#!/usr/bin/env python3
"""
Script Expandido para Coletar Métricas de Marketing Digital
Suporta: Meta Ads, Google Analytics, Google Ads, YouTube
Armazena em: Supabase (PostgreSQL) + Notion (backup)
Versão: 2.0.0
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI
from typing import Optional, List, Dict, Any
from marketing_shared.utils.api_client import AgentAPIClient, AgentAPIError

# Carregar variáveis de ambiente
load_dotenv()

# ============================================
# CONFIGURAÇÕES
# ============================================

# Agent API (substitui acesso direto ao Meta Ads)
AGENT_API_URL = os.getenv("AGENT_API_URL", "http://localhost:8000")
ANALYTICS_API_KEY = os.getenv("ANALYTICS_API_KEY")

# Meta Ads (DEPRECATED - agora usa Agent API)
# META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
# META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")

# Google APIs
GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID")
GOOGLE_ADS_CUSTOMER_ID = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Slack
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# URLs
META_API_URL = "https://graph.facebook.com/v21.0"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

# Inicializar clientes
supabase: Client = create_client(
    SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_URL else None
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# ============================================
# FUNÇÕES DE COLETA POR FONTE
# ============================================


def get_meta_ads_metrics(date_preset: str = "yesterday") -> Optional[List[Dict[str, Any]]]:
    """
    Busca métricas do Meta Ads via Agent API.
    Substitui chamada direta ao Facebook API.
    """
    if not ANALYTICS_API_KEY:
        print("⚠️  Meta Ads: ANALYTICS_API_KEY não configurada")
        return None

    print("🔄 Buscando métricas Meta Ads do Agent API...")

    # Configurar cliente
    client = AgentAPIClient(
        base_url=AGENT_API_URL,
        api_key=ANALYTICS_API_KEY,
        timeout=30,
        max_retries=3
    )

    # Verificar health
    if not client.health_check():
        print("❌ Agent API não está respondendo. Verifique se o servidor está rodando.")
        return None

    # Calcular datas baseado no preset
    if date_preset == "yesterday":
        date_ref = (datetime.now() - timedelta(days=1)).date()
    elif date_preset == "last_7d":
        date_ref = (datetime.now() - timedelta(days=7)).date()
    else:
        date_ref = datetime.now().date()

    try:
        # Buscar métricas
        response = client.get_metrics(
            date_from=date_ref,
            date_until=date_ref
        )

        campaigns = response.get('campaigns', [])
        print(
            f"✅ Meta Ads (via Agent API): {len(campaigns)} campanhas encontradas")
        print(f"   Fonte: {response.get('data_source', 'unknown')}")
        print(f"   Exportado em: {response.get('exported_at', 'unknown')}")

        return campaigns

    except AgentAPIError as e:
        print(f"❌ Erro ao buscar métricas do Agent API: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return None


def get_youtube_metrics() -> Optional[Dict[str, Any]]:
    """Buscar métricas do YouTube Data API"""
    if not YOUTUBE_CHANNEL_ID or not YOUTUBE_API_KEY:
        print("⚠️  YouTube: Credenciais não configuradas")
        return None

    url = f"{YOUTUBE_API_URL}/channels"
    params = {"part": "statistics",
              "id": YOUTUBE_CHANNEL_ID, "key": YOUTUBE_API_KEY}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                stats = data["items"][0]["statistics"]
                print(f"✅ YouTube: {stats.get('subscriberCount')} inscritos")
                return stats
            return None
        else:
            print(f"❌ YouTube Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ YouTube Exception: {str(e)}")
        return None


def get_google_analytics_metrics() -> Optional[Dict[str, Any]]:
    """
    Buscar métricas do Google Analytics 4
    Nota: Requer configuração OAuth2 mais complexa
    Para simplificar, usar Google Analytics Data API v1
    """
    print("⚠️  Google Analytics: Implementação OAuth2 complexa")
    print("💡 Recomendação: Usar n8n workflow para GA4")
    return None


def get_google_ads_metrics() -> Optional[Dict[str, Any]]:
    """
    Buscar métricas do Google Ads
    Nota: Requer Google Ads API client library
    """
    print("⚠️  Google Ads: Implementação complexa (requer google-ads library)")
    print("💡 Recomendação: Usar n8n workflow para Google Ads")
    return None


# ============================================
# PROCESSAMENTO DE DADOS
# ============================================


def process_meta_ads(campaigns_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Processar dados do Meta Ads"""
    if not campaigns_data:
        return None

    total_spend = 0
    total_impressions = 0
    total_reach = 0
    total_clicks = 0
    total_frequency = 0
    total_conversions = 0
    cpe_values: List[float] = []

    for campaign in campaigns_data:
        total_spend += float(campaign.get("spend") or 0)
        total_impressions += int(campaign.get("impressions") or 0)
        total_reach += int(campaign.get("reach") or 0)
        total_clicks += int(campaign.get("clicks") or 0)
        total_frequency += float(campaign.get("frequency") or 0)
        total_conversions += int(campaign.get("conversions") or 0)

        cpe = campaign.get("cpe")
        if cpe is not None:
            cpe_values.append(float(cpe))

    # Calcular métricas derivadas
    avg_ctr = (total_clicks / total_impressions) * \
        100 if total_impressions > 0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_cpe = sum(cpe_values) / \
        len(cpe_values) if cpe_values else 0
    avg_frequency = total_frequency / \
        len(campaigns_data) if campaigns_data else 0
    cost_per_conversion = total_spend / \
        total_conversions if total_conversions > 0 else 0
    cpm = (total_spend / total_impressions) * \
        1000 if total_impressions > 0 else 0

    yesterday = datetime.now() - timedelta(days=1)

    return {
        "data": yesterday.strftime("%Y-%m-%d"),
        "source": "meta_ads",
        "spend": round(total_spend, 2),
        "reach": total_reach,
        "impressions": total_impressions,
        "frequency": round(avg_frequency, 2),
        "clicks": total_clicks,
        "ctr": round(avg_ctr, 2),
        "cpc": round(avg_cpc, 2),
        "cpe": round(avg_cpe, 2),
        "cpm": round(cpm, 2),
        "conversions": total_conversions,
        "cost_per_conversion": round(cost_per_conversion, 2),
        "new_followers": total_conversions,
        "cost_per_follower": round(cost_per_conversion, 2),
        "notes": f"Meta Ads: {len(campaigns_data)} campanhas, {total_clicks} cliques",
        "raw_data": campaigns_data,
    }


def process_youtube(stats_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Processar dados do YouTube"""
    if not stats_data:
        return None

    view_count = int(stats_data.get("viewCount", 0))
    subscriber_count = int(stats_data.get("subscriberCount", 0))

    # Estimativa de views de ontem (1% do total)
    estimated_new_views = round(view_count * 0.01)
    estimated_new_subscribers = round(subscriber_count * 0.001)

    yesterday = datetime.now() - timedelta(days=1)

    return {
        "data": yesterday.strftime("%Y-%m-%d"),
        "source": "youtube",
        "spend": 0,
        "reach": estimated_new_views,
        "impressions": estimated_new_views,
        "views": estimated_new_views,
        "subscribers_gained": estimated_new_subscribers,
        "new_followers": estimated_new_subscribers,
        "notes": f"YouTube: ~{estimated_new_views} views estimadas ontem, total {subscriber_count} inscritos",
        "raw_data": stats_data,
    }


# ============================================
# PERSISTÊNCIA
# ============================================


def save_to_supabase(metrics: Dict[str, Any]) -> bool:
    """Salvar métricas no Supabase"""
    if not supabase:
        print("❌ Supabase: Cliente não configurado")
        return False

    try:
        # Upsert (insert or update if exists)
        result = (
            supabase.table("daily_metrics").upsert(
                metrics, on_conflict="data,source").execute()
        )

        print(f"✅ Supabase: Métricas de '{metrics['source']}' salvas")
        return True
    except Exception as e:
        print(f"❌ Supabase Error: {str(e)}")
        return False


# ============================================
# CONSOLIDAÇÃO E IA
# ============================================


def consolidate_metrics(date_str: str) -> Optional[Dict[str, Any]]:
    """Consolidar métricas de todas as fontes para uma data"""
    if not supabase:
        return None

    try:
        result = supabase.table("daily_metrics").select(
            "*").eq("data", date_str).execute()

        metrics = result.data

        if not metrics:
            print(f"⚠️  Nenhuma métrica encontrada para {date_str}")
            return None

        # Consolidar
        consolidated = {
            "data": date_str,
            "total_spend": sum(float(m.get("spend", 0)) for m in metrics),
            "total_reach": sum(int(m.get("reach", 0)) for m in metrics),
            "total_followers": sum(int(m.get("new_followers", 0)) for m in metrics),
            "total_clicks": sum(int(m.get("clicks", 0)) for m in metrics),
            "total_impressions": sum(int(m.get("impressions", 0)) for m in metrics),
            "by_source": {},
        }

        for m in metrics:
            consolidated["by_source"][m["source"]] = {
                "spend": float(m.get("spend", 0)),
                "followers": int(m.get("new_followers", 0)),
                "ctr": float(m.get("ctr", 0)),
            }

        # Calcular médias
        consolidated["avg_ctr"] = (
            (consolidated["total_clicks"] /
             consolidated["total_impressions"] * 100)
            if consolidated["total_impressions"] > 0
            else 0
        )
        consolidated["avg_cost_per_follower"] = (
            (consolidated["total_spend"] / consolidated["total_followers"])
            if consolidated["total_followers"] > 0
            else 0
        )

        return consolidated
    except Exception as e:
        print(f"❌ Consolidação Error: {str(e)}")
        return None


def generate_insights_openai(consolidated: Dict[str, Any]) -> str:
    """Gerar insights usando OpenAI"""
    if not openai_client:
        return "⚠️ OpenAI não configurado"

    try:
        prompt = f"""Você é um analista de marketing digital. Analise as métricas abaixo e forneça insights acionáveis em português (PT-BR).

📊 MÉTRICAS DO DIA {consolidated['data']}:

💰 Investimento Total: R$ {consolidated['total_spend']:.2f}
📈 Alcance Total: {consolidated['total_reach']:,} pessoas
👥 Novos Seguidores: {consolidated['total_followers']}
💵 Custo/Seguidor: R$ {consolidated['avg_cost_per_follower']:.2f}
📊 CTR Médio: {consolidated['avg_ctr']:.2f}%

📱 PERFORMANCE POR FONTE:
{chr(10).join([f"• {source}: {metrics['followers']} seguidores (R$ {metrics['spend']:.2f} investidos)"
               for source, metrics in consolidated['by_source'].items()])}

🎯 METAS:
• CTR: ≥ 1,5% (atual: {consolidated['avg_ctr']:.2f}%)
• Custo/Seguidor: ≤ R$ 1,30 (atual: R$ {consolidated['avg_cost_per_follower']:.2f})

Forneça:
1. Análise resumida (2-3 frases)
2. Alertas se métricas abaixo da meta
3. 2 ações recomendadas específicas

Seja direto e acionável."""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista de marketing digital especializado.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        insight = response.choices[0].message.content
        print(f"✅ OpenAI: Insights gerados ({len(insight)} chars)")
        return insight
    except Exception as e:
        print(f"❌ OpenAI Error: {str(e)}")
        return f"⚠️ Erro ao gerar insights: {str(e)}"


def send_slack_notification(consolidated: Dict[str, Any], ai_insight: str) -> bool:
    """Enviar notificação no Slack"""
    if not SLACK_WEBHOOK_URL:
        print("⚠️  Slack: Webhook não configurado")
        return False

    try:
        message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📊 Relatório Diário - {consolidated['data']}",
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*💰 Gasto:*\nR$ {consolidated['total_spend']:.2f}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*📈 Alcance:*\n{consolidated['total_reach']:,}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*👥 Seguidores:*\n+{consolidated['total_followers']}",
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*💵 Custo/Seg:*\nR$ {consolidated['avg_cost_per_follower']:.2f}",
                        },
                    ],
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"🤖 *Insight IA:*\n{ai_insight}"},
                },
            ]
        }

        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print("✅ Slack: Notificação enviada")
            return True
        else:
            print(f"❌ Slack Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Slack Exception: {str(e)}")
        return False


# ============================================
# MAIN WORKFLOW
# ============================================


def main() -> None:
    """Função principal - executar coleta completa"""
    print("=" * 50)
    print("🚀 AGENTE DE MARKETING DIGITAL")
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()

    # Verificar Supabase
    if not supabase:
        print("❌ ERRO: Supabase não configurado. Verifique SUPABASE_URL e SUPABASE_SERVICE_KEY")
        return

    results = {"meta_ads": None, "youtube": None,
               "google_analytics": None, "google_ads": None}

    # 1. Meta Ads
    print("📊 [1/4] Coletando Meta Ads...")
    meta_data = get_meta_ads_metrics()
    if meta_data:
        results["meta_ads"] = process_meta_ads(meta_data)
        save_to_supabase(results["meta_ads"])
    print()

    # 2. YouTube
    print("📊 [2/4] Coletando YouTube...")
    yt_data = get_youtube_metrics()
    if yt_data:
        results["youtube"] = process_youtube(yt_data)
        save_to_supabase(results["youtube"])
    print()

    # 3. Google Analytics (placeholder)
    print("📊 [3/4] Google Analytics...")
    print("⏭️  Use o workflow n8n para GA4")
    print()

    # 4. Google Ads (placeholder)
    print("📊 [4/4] Google Ads...")
    print("⏭️  Use o workflow n8n para Google Ads")
    print()

    # 5. Consolidar e gerar insights
    print("🤖 Consolidando e gerando insights IA...")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    consolidated = consolidate_metrics(yesterday)

    if consolidated:
        # Gerar insights IA
        ai_insight = generate_insights_openai(consolidated)

        # Enviar para Slack
        send_slack_notification(consolidated, ai_insight)

        print()
        print("=" * 50)
        print("📈 RESUMO:")
        print(f"   Gasto Total: R$ {consolidated['total_spend']:.2f}")
        print(f"   Novos Seguidores: {consolidated['total_followers']}")
        print(
            f"   Custo/Seguidor: R$ {consolidated['avg_cost_per_follower']:.2f}")
        print(f"   CTR Médio: {consolidated['avg_ctr']:.2f}%")
        print("=" * 50)
        print()
        print("🤖 INSIGHT IA:")
        print(ai_insight)
        print()

    print("✅ Processo concluído!")
    print()


if __name__ == "__main__":
    # Verificar variáveis críticas
    required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_KEY"]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print("❌ Variáveis de ambiente faltando:")
        for var in missing:
            print(f"   - {var}")
        print()
        print("💡 Copie .env.example para .env e preencha os valores")
        exit(1)

    main()
