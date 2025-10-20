#!/usr/bin/env python3
"""
Teste do webhook do Slack
"""

import requests
import json
from datetime import datetime

# Webhook URL do Slack
# Substitua pela sua URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"


def test_simple_message():
    """Testar mensagem simples"""
    message = {
        "text": f"🚀 Teste do Agente Facebook - {datetime.now().strftime('%H:%M:%S')}"
    }

    try:
        print("Enviando mensagem de teste para o Slack...")
        response = requests.post(SLACK_WEBHOOK_URL, json=message)

        if response.status_code == 200:
            print("[OK] Mensagem enviada com sucesso!")
            return True
        else:
            print(f"[ERRO] Falha: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Exceção: {str(e)}")
        return False


def test_rich_message():
    """Testar mensagem rica com blocos"""
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 Relatório Diário - Teste"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": "*💰 Gasto:*\nR$ 25,50"},
                    {"type": "mrkdwn", "text": "*📈 Alcance:*\n1.250"},
                    {"type": "mrkdwn", "text": "*👥 Seguidores:*\n+19"},
                    {"type": "mrkdwn", "text": "*💵 Custo/Seg:*\nR$ 1,34"}
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🤖 *Insight IA:*\nPerformance excelente! CTR acima da meta (1,49% vs 1,5% meta). Custo por seguidor dentro do esperado. Continue assim!\n\n_Teste enviado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}_"
                }
            }
        ]
    }

    try:
        print("Enviando relatório rico para o Slack...")
        response = requests.post(SLACK_WEBHOOK_URL, json=message)

        if response.status_code == 200:
            print("[OK] Relatório rico enviado com sucesso!")
            return True
        else:
            print(f"[ERRO] Falha: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"[ERRO] Exceção: {str(e)}")
        return False


def main():
    """Função principal"""
    print("="*60)
    print("TESTE DO SLACK WEBHOOK")
    print("="*60)

    # Teste 1: Mensagem simples
    print("\n[TESTE 1] Mensagem simples...")
    if test_simple_message():
        print("[OK] Mensagem simples funcionando!")
    else:
        print("[ERRO] Problema na mensagem simples")
        return

    print("\n" + "="*40)

    # Teste 2: Mensagem rica
    print("\n[TESTE 2] Relatório rico...")
    if test_rich_message():
        print("[OK] Relatório rico funcionando!")
    else:
        print("[ERRO] Problema no relatório rico")
        return

    print("\n" + "="*60)
    print("[SUCESSO] SLACK WEBHOOK CONFIGURADO E FUNCIONANDO!")
    print("\nProximos passos:")
    print("   1. [OK] Supabase configurado")
    print("   2. [OK] Slack webhook configurado")
    print("   3. [PENDENTE] Configurar Google APIs")
    print("   4. [PENDENTE] Configurar OpenAI")
    print("   5. [PENDENTE] Importar workflows n8n")
    print("   6. [PENDENTE] Instalar Apache Superset")
    print("="*60)


if __name__ == "__main__":
    main()
