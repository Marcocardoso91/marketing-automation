#!/usr/bin/env python3
"""
Teste de conexão com Supabase
Verifica se a API está funcionando
"""

import requests
import json

# Credenciais do Supabase
SUPABASE_URL = "https://zzpjqldhosgaxyjpcvqc.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6cGpxbGRob3NnYXh5anBjdnFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDc1OTQ4NiwiZXhwIjoyMDc2MzM1NDg2fQ.pUAcpdaHe8qffgwKg3yLdPpcmXOdFVWwoEj7RVAIKvk"


def test_connection():
    """Testar conexão com Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }

    try:
        print("Testando conexao com Supabase...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("[OK] Conexao com Supabase funcionando!")
            print(f"   URL: {SUPABASE_URL}")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"[ERRO] Conexao falhou: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Excecao na conexao: {str(e)}")
        return False


def test_table_exists():
    """Testar se a tabela daily_metrics existe"""
    url = f"{SUPABASE_URL}/rest/v1/daily_metrics?select=count"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }

    try:
        print("Verificando se tabela daily_metrics existe...")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print("[OK] Tabela daily_metrics existe e esta acessivel!")
            data = response.json()
            print(
                f"   Total de registros: {len(data) if isinstance(data, list) else 'N/A'}")
            return True
        elif response.status_code == 404:
            print("[AVISO] Tabela daily_metrics nao existe ainda.")
            print("   Execute o SQL no Supabase SQL Editor primeiro.")
            return False
        else:
            print(f"[ERRO] Erro ao verificar tabela: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Excecao ao verificar tabela: {str(e)}")
        return False


def insert_test_data():
    """Inserir dados de teste"""
    url = f"{SUPABASE_URL}/rest/v1/daily_metrics"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=ignore-duplicates"
    }

    test_data = {
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
    }

    try:
        print("Inserindo dados de teste...")
        response = requests.post(url, headers=headers, json=test_data)

        if response.status_code in [200, 201]:
            print("[OK] Dados de teste inseridos com sucesso!")
            return True
        else:
            print(
                f"[AVISO] Inserção: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Erro ao inserir dados: {str(e)}")
        return False


def main():
    """Função principal"""
    print("="*60)
    print("TESTE DE CONEXAO COM SUPABASE")
    print("="*60)

    # Teste 1: Conexão
    if not test_connection():
        print("\n[ERRO] Nao foi possivel conectar ao Supabase.")
        print("   Verifique as credenciais e URL.")
        return

    print()

    # Teste 2: Tabela existe?
    if not test_table_exists():
        print("\n[INSTRUCOES] Para criar a tabela:")
        print("   1. Acesse: https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc")
        print("   2. Vá em SQL Editor")
        print("   3. Cole o conteúdo do arquivo SQL-PARA-SUPABASE.sql")
        print("   4. Execute o SQL")
        print("   5. Execute este script novamente")
        return

    print()

    # Teste 3: Inserir dados
    if insert_test_data():
        print("\n[OK] SUPABASE CONFIGURADO E FUNCIONANDO!")
        print("\nProximos passos:")
        print("   1. [OK] Supabase configurado")
        print("   2. [PENDENTE] Configurar Slack webhook")
        print("   3. [PENDENTE] Configurar Google APIs")
        print("   4. [PENDENTE] Configurar OpenAI")
        print("   5. [PENDENTE] Importar workflows n8n")
        print("   6. [PENDENTE] Instalar Apache Superset")
    else:
        print("\n[AVISO] Supabase conectado mas com problemas na inserção.")

    print("="*60)


if __name__ == "__main__":
    main()
