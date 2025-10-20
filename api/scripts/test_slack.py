#!/usr/bin/env python3
"""
Teste específico para Slack
"""
import requests
import os
import sys
from pathlib import Path

# Carregar .env
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"

if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value


def test_slack():
    """Testar envio para Slack"""
    print("TESTE SLACK - Facebook Ads AI Agent")
    print("=" * 40)

    slack_url = os.getenv("SLACK_WEBHOOK_URL")

    if not slack_url:
        print("[ERRO] SLACK_WEBHOOK_URL não encontrado")
        return False

    print(f"URL: {slack_url}")

    # Mensagem de teste
    message = {
        "text": "🧪 *TESTE* - Facebook Ads AI Agent",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "🧪 *TESTE* - Facebook Ads AI Agent\n\n✅ Sistema de alertas funcionando!\n📱 WhatsApp: OK\n💬 Slack: Testando...\n📝 Notion: Pendente\n📧 Email: Pendente"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Campanha:*\nTeste de Integração"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Score:*\n85/100"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*CTR:*\n2.5%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Status:*\n✅ Funcionando"
                    }
                ]
            }
        ]
    }

    try:
        print("Enviando mensagem para Slack...")
        response = requests.post(slack_url, json=message, timeout=10)

        if response.status_code == 200:
            print("[OK] Mensagem enviada com sucesso!")
            print("Verifique o canal #facebook-ads-alerts no Slack")
            return True
        else:
            print(f"[ERRO] Status: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Falha ao enviar: {e}")
        return False


if __name__ == "__main__":
    success = test_slack()
    if success:
        print("\n🎉 SLACK CONFIGURADO COM SUCESSO!")
    else:
        print("\n❌ Problema na configuração do Slack")
