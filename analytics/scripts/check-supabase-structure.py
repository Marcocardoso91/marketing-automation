#!/usr/bin/env python3
"""
Verificar estrutura completa do Supabase
"""

import requests
import json

# Credenciais
SUPABASE_URL = "https://zzpjqldhosgaxyjpcvqc.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6cGpxbGRob3NnYXh5anBjdnFjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDc1OTQ4NiwiZXhwIjoyMDc2MzM1NDg2fQ.pUAcpdaHe8qffgwKg3yLdPpcmXOdFVWwoEj7RVAIKvk"

def check_table(table_name):
    """Verificar se tabela existe e quantos registros tem"""
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select=*&limit=5"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] {table_name}: {len(data)} registros (mostrando max 5)")
            if data:
                print(f"   Exemplo: {json.dumps(data[0], indent=2, default=str)[:200]}...")
            return True
        else:
            print(f"[ERRO] {table_name}: Nao existe ou erro {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERRO] {table_name}: Erro {str(e)}")
        return False

def main():
    print("="*60)
    print("VERIFICAÇÃO COMPLETA DO SUPABASE")
    print("="*60)
    print()

    # Verificar tabelas e views
    tables = [
        "daily_metrics",
        "metrics_consolidated",
        "performance_by_source",
        "weekly_summary"
    ]

    for table in tables:
        check_table(table)
        print()

    print("="*60)

if __name__ == "__main__":
    main()
