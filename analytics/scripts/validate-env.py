#!/usr/bin/env python3
"""
Script de validação de variáveis de ambiente
Valida se todas as variáveis necessárias estão configuradas
"""

import os
import sys

# Variáveis obrigatórias (P0)
REQUIRED_VARS = [
    "SUPABASE_URL",
    "SUPABASE_SERVICE_KEY",
    "META_ACCESS_TOKEN",
    "META_AD_ACCOUNT_ID",
]

# Variáveis opcionais (P1/P2)
OPTIONAL_VARS = [
    "GA4_PROPERTY_ID",
    "GOOGLE_ADS_CUSTOMER_ID",
    "YOUTUBE_CHANNEL_ID",
    "YOUTUBE_API_KEY",
    "OPENAI_API_KEY",
    "SLACK_WEBHOOK_URL",
    "NOTION_TOKEN",
    "NOTION_DATABASE_ID",
]


def validate_env() -> bool:
    """Valida variáveis de ambiente necessárias"""
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]

    if missing:
        print("ERRO: Variaveis obrigatorias faltando:")
        for var in missing:
            print(f"   - {var}")
        return False

    print("OK: Todas variaveis obrigatorias configuradas!")

    # Verificar opcionais
    missing_optional = [var for var in OPTIONAL_VARS if not os.getenv(var)]
    if missing_optional:
        print("\nATENCAO: Variaveis opcionais nao configuradas:")
        for var in missing_optional:
            print(f"   - {var}")
        print("\nDICA: Estas sao opcionais mas recomendadas para funcionalidade completa")

    return True


def show_env_status() -> None:
    """Mostra status de todas as variáveis"""
    print("=" * 50)
    print("STATUS DAS VARIAVEIS DE AMBIENTE")
    print("=" * 50)
    print()

    print("OBRIGATORIAS:")
    for var in REQUIRED_VARS:
        value = os.getenv(var)
        status = "OK" if value else "FALTANDO"
        masked_value = "***" + \
            value[-4:] if value and len(value) > 4 else "N/A"
        print(f"   {status}: {var} = {masked_value}")

    print("\nOPCIONAIS:")
    for var in OPTIONAL_VARS:
        value = os.getenv(var)
        status = "OK" if value else "NAO CONFIGURADO"
        masked_value = "***" + \
            value[-4:] if value and len(value) > 4 else "N/A"
        print(f"   {status}: {var} = {masked_value}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    show_env_status()
    print()

    success = validate_env()

    if success:
        print("\nSUCESSO: Ambiente configurado corretamente!")
        sys.exit(0)
    else:
        print("\nDICA: Copie .env.example para .env e preencha os valores obrigatorios")
        sys.exit(1)
