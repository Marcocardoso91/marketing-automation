#!/usr/bin/env python3
"""
Script para testar todas as integrações de alertas
WhatsApp, Slack, Email e Notion
"""
from src.utils.logger import setup_logger
from src.integrations.notion_client import get_notion_client
from src.integrations.n8n_client import get_n8n_client
import asyncio
import os
import sys
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


logger = setup_logger(__name__)


async def test_whatsapp():
    """Testar integração WhatsApp"""
    print("[TESTE] Testando WhatsApp...")

    try:
        n8n = get_n8n_client()
        whatsapp_phone = os.getenv("WHATSAPP_ALERT_PHONE")

        if not whatsapp_phone:
            print("[ERRO] WHATSAPP_ALERT_PHONE não configurado no .env")
            return False

        result = await n8n.trigger_workflow("whatsapp-evolution", {
            "phone": whatsapp_phone,
            "message": """
🧪 *TESTE* - Facebook Ads AI Agent

Sistema de alertas funcionando!

✅ WhatsApp: OK
⏳ Slack: Pendente
⏳ Email: Pendente  
⏳ Notion: Pendente

Teste realizado em: """ + str(asyncio.get_event_loop().time())
        })

        if result:
            print(f"✅ WhatsApp enviado com sucesso para {whatsapp_phone}")
            return True
        else:
            print("❌ Falha ao enviar WhatsApp")
            return False

    except Exception as e:
        print(f"❌ Erro no teste WhatsApp: {e}")
        return False


async def test_notion():
    """Testar integração Notion"""
    print("🧪 Testando Notion...")

    try:
        notion_db_id = os.getenv("NOTION_DATABASE_ID")

        if not notion_db_id or notion_db_id == "abc123def456":
            print("❌ NOTION_DATABASE_ID não configurado (ainda é placeholder)")
            print("   Precisa criar database no Notion primeiro")
            return False

        notion = get_notion_client(notion_db_id)

        # Teste simples - salvar sugestão
        result = await notion.save_suggestion({
            'campaign_id': 'test-123',
            'campaign_name': 'Teste de Integração',
            'type': 'TEST',
            'reason': 'Teste do sistema de alertas',
            'data': {
                'ctr': 1.5,
                'cpa': 45.0,
                'spend': 100.0
            }
        })

        if result:
            print(f"✅ Notion: Página criada com sucesso")
            print(f"   URL: {result}")
            return True
        else:
            print("❌ Falha ao criar página no Notion")
            return False

    except Exception as e:
        print(f"❌ Erro no teste Notion: {e}")
        return False


async def test_n8n_connection():
    """Testar conexão com n8n"""
    print("🧪 Testando conexão n8n...")

    try:
        n8n = get_n8n_client()

        # Testar listagem de workflows
        workflows = await n8n.list_workflows()

        if workflows:
            print(f"✅ n8n conectado: {len(workflows)} workflows encontrados")

            # Mostrar workflows ativos
            active_workflows = [w for w in workflows if w.get('active', False)]
            print(f"   Workflows ativos: {len(active_workflows)}")

            for wf in active_workflows[:3]:  # Mostrar apenas 3
                print(
                    f"   - {wf.get('name', 'Sem nome')} (ID: {wf.get('id', 'N/A')})")

            return True
        else:
            print("❌ Nenhum workflow encontrado no n8n")
            return False

    except Exception as e:
        print(f"❌ Erro na conexão n8n: {e}")
        return False


async def test_slack_config():
    """Verificar configuração Slack"""
    print("🧪 Verificando configuração Slack...")

    slack_url = os.getenv("SLACK_WEBHOOK_URL")

    if not slack_url or "XXX" in slack_url:
        print("❌ SLACK_WEBHOOK_URL não configurado")
        print("   Precisa configurar webhook no Slack primeiro")
        return False
    else:
        print("✅ SLACK_WEBHOOK_URL configurado")
        print("   (Teste real requer webhook válido)")
        return True


def print_config_status():
    """Mostrar status das configurações"""
    print("\n" + "="*60)
    print("📋 STATUS DAS CONFIGURAÇÕES")
    print("="*60)

    configs = {
        "WHATSAPP_ALERT_PHONE": os.getenv("WHATSAPP_ALERT_PHONE"),
        "SLACK_WEBHOOK_URL": os.getenv("SLACK_WEBHOOK_URL"),
        "ADMIN_EMAIL": os.getenv("ADMIN_EMAIL"),
        "NOTION_API_TOKEN": os.getenv("NOTION_API_TOKEN"),
        "NOTION_DATABASE_ID": os.getenv("NOTION_DATABASE_ID"),
        "N8N_API_URL": os.getenv("N8N_API_URL"),
        "N8N_API_KEY": os.getenv("N8N_API_KEY")
    }

    for key, value in configs.items():
        if value:
            if "XXX" in str(value) or "abc123" in str(value):
                status = "⚠️  PLACEHOLDER"
            else:
                status = "✅ CONFIGURADO"
        else:
            status = "❌ FALTANDO"

        print(f"{status} {key}")


async def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO DE INTEGRAÇÕES")
    print("Facebook Ads AI Agent - Sistema de Alertas")
    print("="*60)

    # Carregar .env se existir
    env_file = Path(".env")
    if env_file.exists():
        print("📁 Arquivo .env encontrado")
        # Carregar variáveis
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    else:
        print("❌ Arquivo .env não encontrado")
        return

    print_config_status()

    print("\n" + "="*60)
    print("🧪 EXECUTANDO TESTES")
    print("="*60)

    # Executar testes
    results = {}

    results['n8n'] = await test_n8n_connection()
    results['whatsapp'] = await test_whatsapp()
    results['notion'] = await test_notion()
    results['slack'] = test_slack_config()

    # Resumo final
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)

    for test, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} {test.upper()}")

    passed = sum(results.values())
    total = len(results)

    print(f"\n🎯 RESULTADO: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 TODAS AS INTEGRAÇÕES FUNCIONANDO!")
    elif passed >= 2:
        print("⚠️  Algumas integrações funcionando - verificar configurações")
    else:
        print("❌ Muitas integrações com problemas - verificar .env")

if __name__ == "__main__":
    asyncio.run(main())
