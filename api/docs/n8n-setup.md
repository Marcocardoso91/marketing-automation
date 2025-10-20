# n8n Setup Guide

Guia para configurar workflows n8n do Facebook Ads AI Agent.

## Acesso ao n8n

- **URL Dev:** http://localhost:5678
- **URL Prod:** https://n8n.fbads.example.com
- **Credenciais:** admin / admin (padrão, altere em produção!)

## Workflows Disponíveis

### 1. fb_fetch_metrics

**Objetivo:** Coletar métricas do Facebook Ads a cada 30 minutos

**Importar:**
1. Acesse n8n → Workflows → Import from File
2. Selecione `config/n8n/workflows/fb_fetch_metrics.json`
3. Clique em "Import"

**Configurar:**
1. Node "Facebook API" → Credentials
2. Adicionar credencial tipo "Facebook Graph API"
3. Inserir Access Token do Facebook
4. Salvar e ativar workflow

**Testar:**
```bash
curl -X POST http://localhost:5678/webhook/fb_fetch_metrics \
  -H "Content-Type: application/json" \
  -d '{"account_id": "act_123456789"}'
```

**Esperado:** Resposta `{"success": true, "campaigns_processed": N}`

### 2. send_alerts_multi

**Objetivo:** Enviar alertas via Slack e Email

**Importar:**
1. n8n → Workflows → Import from File
2. Selecione `config/n8n/workflows/send_alerts_multi.json`
3. Import

**Configurar:**

**Slack:**
1. Criar Incoming Webhook no Slack: https://api.slack.com/messaging/webhooks
2. Copiar Webhook URL
3. Node "Send to Slack" → URL → Colar webhook
4. Salvar

**Email:**
1. Node "Send Email" → Credentials
2. Adicionar credencial SMTP (SendGrid, AWS SES, etc.)
3. Configurar From/To emails
4. Salvar

**Testar:**
```bash
curl -X POST http://localhost:5678/webhook/send_alerts_multi \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "123",
    "campaign_name": "Test Campaign",
    "issue_type": "CTR_BAIXO",
    "severity": "WARNING",
    "metrics": {"ctr": 0.5, "cpa": 60, "spend": 100},
    "timestamp": "2025-10-18T10:00:00"
  }'
```

**Esperado:** Mensagem no Slack e Email recebido

### 3. build_recommendations (TODO)

**Objetivo:** Gerar recomendações de otimização

**Status:** A implementar em Sprint 3

### 4. calendar_context (TODO)

**Objetivo:** Enriquecer com contexto de calendário

**Status:** A implementar em Sprint 3

## Credentials Necessárias

### Facebook Graph API
- **Type:** OAuth2 / Personal Access Token
- **Access Token:** Seu token do Facebook
- **Scope:** ads_read, ads_management

### Slack
- **Type:** Webhook URL
- **URL:** https://hooks.slack.com/services/YOUR/WEBHOOK/URL

### SMTP (Email)
- **Type:** SMTP
- **Host:** smtp.sendgrid.net (ou outro)
- **Port:** 587
- **User:** apikey (SendGrid) ou seu usuário
- **Password:** Sua API key

### Google Calendar (Futuro)
- **Type:** OAuth2
- **Client ID:** Seu client ID do Google Cloud
- **Client Secret:** Seu client secret
- **Scope:** https://www.googleapis.com/auth/calendar.readonly

## Troubleshooting

### Workflow não executa

1. Verificar se workflow está ativo (toggle verde)
2. Verificar logs do n8n: `docker-compose logs n8n`
3. Testar manualmente clicando em "Execute Workflow"

### Erro de autenticação

1. Revalidar credentials
2. Verificar se token Facebook não expirou
3. Gerar novo token se necessário

### Webhook não responde

1. Verificar URL do webhook (deve incluir /webhook/)
2. Verificar se container n8n está rodando
3. Verificar network connectivity entre containers

## Backup e Versionamento

### Exportar Workflows

```bash
# Via UI
n8n → Workflows → ... (menu) → Download

# Via CLI (dentro do container)
docker-compose exec n8n n8n export:workflow --all --output=/workflows/
```

### Importar Workflows

```bash
# Via UI
n8n → Workflows → Import from File

# Via CLI
docker-compose exec n8n n8n import:workflow --input=/workflows/fb_fetch_metrics.json
```

### Versionar no Git

```bash
# Exportar workflows para config/n8n/workflows/
# Commitar no Git
git add config/n8n/workflows/
git commit -m "Update n8n workflows"
git push
```

## Melhores Práticas

1. **Sempre testar workflows manualmente** antes de ativar
2. **Manter backups** de workflows críticos
3. **Versionar workflows no Git** após mudanças
4. **Documentar mudanças** no changelog do workflow
5. **Usar variáveis de ambiente** para credentials sensíveis
6. **Monitorar execuções** via Executions tab no n8n

## Referencias

- **n8n Docs:** https://docs.n8n.io/
- **Facebook API:** https://developers.facebook.com/docs/marketing-api/
- **Webhooks:** https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/

---

**Atualizado:** Outubro 2025

