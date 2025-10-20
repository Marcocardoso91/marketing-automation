#!/usr/bin/env python3
"""
Script simples para testar integrações (sem emojis)
"""
import asyncio
import os
import sys
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_env():
    """Carregar variáveis do .env"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("Arquivo .env carregado")
    else:
        print("Arquivo .env não encontrado")


async def test_whatsapp():
    """Testar WhatsApp"""
    print("\n[TESTE] WhatsApp...")

    try:
        from src.integrations.n8n_client import get_n8n_client

        n8n = get_n8n_client()
        whatsapp_phone = os.getenv("WHATSAPP_ALERT_PHONE")

        if not whatsapp_phone:
            print("[ERRO] WHATSAPP_ALERT_PHONE não configurado")
            return False

        print(f"Enviando para: {whatsapp_phone}")

        result = await n8n.trigger_workflow("evolution-webhook", {
            "phone": whatsapp_phone,
            "message": "TESTE - Facebook Ads AI Agent - Sistema funcionando!"
        })

        if result:
            print("[OK] WhatsApp enviado com sucesso")
            return True
        else:
            print("[ERRO] Falha ao enviar WhatsApp")
            return False

    except Exception as e:
        print(f"[ERRO] WhatsApp: {e}")
        return False


async def test_n8n():
    """Testar conexão n8n"""
    print("\n[TESTE] n8n...")

    try:
        from src.integrations.n8n_manager import N8nWorkflowManager

        n8n = N8nWorkflowManager()
        workflows = await n8n.list_workflows()

        if workflows:
            print(f"[OK] n8n conectado: {len(workflows)} workflows")
            active = [w for w in workflows if w.get('active', False)]
            print(f"Workflows ativos: {len(active)}")
            return True
        else:
            print("[ERRO] Nenhum workflow encontrado")
            return False

    except Exception as e:
        print(f"[ERRO] n8n: {e}")
        return False


def test_config():
    """Verificar configurações"""
    print("\n[CONFIG] Verificando configurações...")

    configs = {
        "WHATSAPP_ALERT_PHONE": os.getenv("WHATSAPP_ALERT_PHONE"),
        "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL"),
        "NOTION_API_TOKEN": os.getenv("NOTION_API_TOKEN"),
        "N8N_API_KEY": os.getenv("N8N_API_KEY")
    }

    for key, value in configs.items():
        if value and "XXX" not in str(value) and "abc123" not in str(value):
            print(f"[OK] {key}")
        else:
            print(f"[PENDENTE] {key}")


async def main():
    """Função principal"""
    print("TESTE DE INTEGRACOES - Facebook Ads AI Agent")
    print("=" * 50)

    load_env()
    test_config()

    results = {}
    results['n8n'] = await test_n8n()
    results['whatsapp'] = await test_whatsapp()

    print("\n" + "=" * 50)
    print("RESUMO:")
    for test, result in results.items():
        status = "OK" if result else "ERRO"
        print(f"{test.upper()}: {status}")

    passed = sum(results.values())
    total = len(results)
    print(f"\nRESULTADO: {passed}/{total} testes passaram")

if __name__ == "__main__":
    asyncio.run(main())
