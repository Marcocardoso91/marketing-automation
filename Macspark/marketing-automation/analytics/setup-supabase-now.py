#!/usr/bin/env python3
"""
Script para configurar Supabase automaticamente
Usa as credenciais fornecidas pelo usuário
"""

import requests
import json
from datetime import datetime

# Credenciais do Supabase (fornecidas pelo usuário)
SUPABASE_URL = "https://zzpjqldhosgaxyjpcvqc.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6cGpxbGRob3NnYXh5anBjdnFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDc1OTQ4NiwiZXhwIjoyMDc2MzM1NDg2fQ.pUAcpdaHe8qffgwKg3yLdPpcmXOdFVWwoEj7RVAIKvk"


def execute_sql(sql_query, description):
    """Executar SQL no Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"

    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    data = {
        "sql": sql_query
    }

    try:
        print(f"[INFO] {description}...")
        response = requests.post(url, headers=headers, json=data)

        if response.status_code in [200, 201, 204]:
            print(f"[OK] {description} - SUCESSO!")
            return True
        else:
            print(f"[ERRO] {description} - ERRO: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] {description} - EXCEÇÃO: {str(e)}")
        return False


def create_table_daily_metrics():
    """Criar tabela daily_metrics"""
    sql = """
    CREATE TABLE IF NOT EXISTS daily_metrics (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        source VARCHAR(50) NOT NULL,
        spend DECIMAL(10,2) DEFAULT 0,
        reach INTEGER DEFAULT 0,
        impressions INTEGER DEFAULT 0,
        clicks INTEGER DEFAULT 0,
        ctr DECIMAL(5,2) DEFAULT 0,
        cpc DECIMAL(10,4) DEFAULT 0,
        cpm DECIMAL(10,2) DEFAULT 0,
        frequency DECIMAL(5,2) DEFAULT 0,
        conversions INTEGER DEFAULT 0,
        new_followers INTEGER DEFAULT 0,
        cost_per_conversion DECIMAL(10,2) DEFAULT 0,
        cost_per_follower DECIMAL(10,2) DEFAULT 0,
        views INTEGER DEFAULT 0,
        subscribers_gained INTEGER DEFAULT 0,
        sessions INTEGER DEFAULT 0,
        users INTEGER DEFAULT 0,
        bounce_rate DECIMAL(5,2) DEFAULT 0,
        notes TEXT,
        raw_data JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        UNIQUE(data, source)
    );
    """
    return execute_sql(sql, "Criando tabela daily_metrics")


def create_indexes():
    """Criar índices para performance"""
    indexes = [
        ("CREATE INDEX IF NOT EXISTS idx_daily_metrics_data ON daily_metrics(data);",
         "Criando índice por data"),
        ("CREATE INDEX IF NOT EXISTS idx_daily_metrics_source ON daily_metrics(source);",
         "Criando índice por fonte"),
        ("CREATE INDEX IF NOT EXISTS idx_daily_metrics_data_source ON daily_metrics(data, source);",
         "Criando índice composto")
    ]

    success = True
    for sql, desc in indexes:
        if not execute_sql(sql, desc):
            success = False

    return success


def create_views():
    """Criar views para análise"""
    views = [
        ("""
        CREATE OR REPLACE VIEW metrics_consolidated AS
        SELECT 
            data,
            COUNT(*) as sources_count,
            SUM(spend) as total_spend,
            SUM(reach) as total_reach,
            SUM(impressions) as total_impressions,
            SUM(clicks) as total_clicks,
            SUM(new_followers) as total_new_followers,
            SUM(conversions) as total_conversions,
            CASE 
                WHEN SUM(impressions) > 0 THEN (SUM(clicks)::DECIMAL / SUM(impressions)) * 100 
                ELSE 0 
            END as avg_ctr,
            CASE 
                WHEN SUM(clicks) > 0 THEN SUM(spend) / SUM(clicks) 
                ELSE 0 
            END as avg_cpc,
            CASE 
                WHEN SUM(impressions) > 0 THEN (SUM(spend) / SUM(impressions)) * 1000 
                ELSE 0 
            END as avg_cpm,
            CASE 
                WHEN SUM(new_followers) > 0 THEN SUM(spend) / SUM(new_followers) 
                ELSE 0 
            END as avg_cost_per_follower,
            STRING_AGG(
                source || ': R$' || spend::TEXT || ' (' || new_followers::TEXT || ' seguidores)',
                ', '
            ) as performance_by_source,
            created_at
        FROM daily_metrics
        GROUP BY data, created_at
        ORDER BY data DESC;
        """, "Criando view metrics_consolidated"),

        ("""
        CREATE OR REPLACE VIEW performance_by_source AS
        SELECT 
            source,
            COUNT(*) as days_tracked,
            AVG(spend) as avg_daily_spend,
            AVG(new_followers) as avg_daily_followers,
            AVG(ctr) as avg_ctr,
            AVG(cpc) as avg_cpc,
            AVG(cost_per_follower) as avg_cost_per_follower,
            SUM(spend) as total_spend,
            SUM(new_followers) as total_followers,
            CASE 
                WHEN SUM(spend) > 0 AND SUM(new_followers) > 0 
                THEN (SUM(new_followers) * 1.30) / SUM(spend)
                ELSE 0 
            END as estimated_roi,
            MAX(data) as last_update
        FROM daily_metrics
        WHERE spend > 0 OR new_followers > 0
        GROUP BY source
        ORDER BY total_followers DESC;
        """, "Criando view performance_by_source")
    ]

    success = True
    for sql, desc in views:
        if not execute_sql(sql, desc):
            success = False

    return success


def insert_test_data():
    """Inserir dados de teste"""
    test_data = [
        {
            "data": "2025-10-17",
            "source": "meta_ads",
            "spend": 25.50,
            "reach": 1250,
            "impressions": 8500,
            "clicks": 127,
            "ctr": 1.49,
            "cpc": 0.20,
            "new_followers": 19,
            "cost_per_follower": 1.34,
            "notes": "Dados de teste - Meta Ads"
        },
        {
            "data": "2025-10-17",
            "source": "youtube",
            "spend": 0.00,
            "reach": 450,
            "impressions": 450,
            "clicks": 0,
            "ctr": 0.00,
            "cpc": 0.00,
            "new_followers": 3,
            "cost_per_follower": 0.00,
            "notes": "Dados de teste - YouTube"
        }
    ]

    url = f"{SUPABASE_URL}/rest/v1/daily_metrics"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=ignore-duplicates"
    }

    try:
        print("[INFO] Inserindo dados de teste...")
        response = requests.post(url, headers=headers, json=test_data)

        if response.status_code in [200, 201]:
            print("[OK] Dados de teste inseridos com sucesso!")
            return True
        else:
            print(
                f"[AVISO] Dados de teste: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Erro ao inserir dados de teste: {str(e)}")
        return False


def verify_setup():
    """Verificar se a configuração foi bem-sucedida"""
    url = f"{SUPABASE_URL}/rest/v1/daily_metrics?select=count"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }

    try:
        print("[INFO] Verificando configuração...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(
                f"[OK] Verificação concluída! Tabela daily_metrics está funcionando.")
            print(
                f"   Total de registros: {len(data) if isinstance(data, list) else 'N/A'}")
            return True
        else:
            print(f"[ERRO] Erro na verificação: {response.status_code}")
            return False

    except Exception as e:
        print(f"[ERRO] Erro na verificação: {str(e)}")
        return False


def main():
    """Função principal"""
    print("="*60)
    print("CONFIGURACAO AUTOMATICA DO SUPABASE")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {SUPABASE_URL}")
    print("="*60)
    print()

    steps = [
        ("Criando tabela daily_metrics", create_table_daily_metrics),
        ("Criando índices", create_indexes),
        ("Criando views", create_views),
        ("Inserindo dados de teste", insert_test_data),
        ("Verificando configuração", verify_setup)
    ]

    success_count = 0
    total_steps = len(steps)

    for step_name, step_function in steps:
        print(f"\n[PASSO] {step_name}...")
        if step_function():
            success_count += 1
        print()

    print("="*60)
    print("RESUMO DA CONFIGURACAO:")
    print(f"   Passos executados: {success_count}/{total_steps}")
    print(f"   Taxa de sucesso: {(success_count/total_steps)*100:.1f}%")

    if success_count == total_steps:
        print("[OK] CONFIGURACAO COMPLETA COM SUCESSO!")
        print()
        print("PROXIMOS PASSOS:")
        print("   1. [OK] Supabase configurado")
        print("   2. [PENDENTE] Configurar Slack webhook")
        print("   3. [PENDENTE] Configurar Google APIs")
        print("   4. [PENDENTE] Configurar OpenAI")
        print("   5. [PENDENTE] Importar workflows n8n")
        print("   6. [PENDENTE] Instalar Apache Superset")
    else:
        print("[AVISO] CONFIGURACAO PARCIAL - Verificar erros acima")

    print("="*60)


if __name__ == "__main__":
    main()
