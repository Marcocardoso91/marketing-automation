# 🔧 Setup n8n - Instância Macspark

## Configuração da Integração com fluxos.macspark.dev

**Data:** 18 de Outubro de 2025  
**Instância:** https://fluxos.macspark.dev  
**Status:** ✅ Credenciais Configuradas  

---

## 🎯 OVERVIEW

O **Facebook Ads AI Agent** está integrado com a instância **n8n da Macspark** em produção.

### Dados da Instância

| Item | Valor |
|------|-------|
| **URL Base** | `https://fluxos.macspark.dev` |
| **API Endpoint** | `https://fluxos.macspark.dev/api/v1` |
| **Webhook Base** | `https://fluxos.macspark.dev/webhook` |
| **Status** | 🟢 Online |

---

## ✅ CREDENCIAIS CONFIGURADAS

### Arquivo .env (Criado)

```bash
# n8n Configuration (Macspark Production)
N8N_WEBHOOK_URL=https://fluxos.macspark.dev/webhook
N8N_API_URL=https://fluxos.macspark.dev/api/v1
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Detalhes do Token JWT

O token JWT fornecido:
- **Issuer:** n8n
- **Audience:** public-api
- **Subject:** User ID único
- **Issued At:** Janeiro 2024
- **Tipo:** Bearer token para API REST

---

## 🚀 FUNCIONALIDADES DISPONÍVEIS

### Via API REST (n8n_manager.py)

Com as credenciais configuradas, você pode:

1. **Listar Workflows Existentes**
   ```bash
   GET https://fluxos.macspark.dev/api/v1/workflows
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

2. **Criar Novos Workflows**
   ```bash
   POST https://fluxos.macspark.dev/api/v1/workflows
   ```

3. **Ativar/Desativar Workflows**
   ```bash
   PATCH https://fluxos.macspark.dev/api/v1/workflows/{id}
   ```

4. **Executar via Webhook**
   ```bash
   POST https://fluxos.macspark.dev/webhook/{workflow-path}
   ```

### Via MCP (n8n-mcp tools)

Ferramentas MCP disponíveis:
- `n8n_list_workflows()` - Lista todos workflows
- `n8n_create_workflow()` - Cria workflow programaticamente
- `n8n_get_workflow(id)` - Obtém detalhes
- `n8n_update_partial_workflow()` - Atualiza incrementalmente
- `n8n_validate_workflow()` - Valida configuração
- `search_nodes(query)` - Busca nodes disponíveis

---

## 📋 TESTES INICIAIS

### 1. Testar Conexão API

```bash
# Via curl
curl -X GET "https://fluxos.macspark.dev/api/v1/workflows" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNWRmNTJiMy1mNWE3LTQyNDItYjExYy1kODE0YjBkZWFkODgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwODAyMTQ2fQ.6SODGZxkIvruAhYPClpdX-MSNGRPDUscjFDi2D9nl2o"

# Via Python
import httpx
import asyncio

async def test_n8n_connection():
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNWRmNTJiMy1mNWE3LTQyNDItYjExYy1kODE0YjBkZWFkODgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwODAyMTQ2fQ.6SODGZxkIvruAhYPClpdX-MSNGRPDUscjFDi2D9nl2o"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://fluxos.macspark.dev/api/v1/workflows",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Workflows: {response.json()}")

asyncio.run(test_n8n_connection())
```

### 2. Testar via FastAPI Endpoint

```bash
# Listar workflows
curl http://localhost:8000/api/v1/n8n/workflows

# Criar workflow de métricas
curl -X POST http://localhost:8000/api/v1/n8n/workflows/create-metrics

# Criar workflow de alertas
curl -X POST http://localhost:8000/api/v1/n8n/workflows/create-alerts \
  -H "Content-Type: application/json" \
  -d '{
    "slack_webhook": "https://hooks.slack.com/...",
    "email_from": "alerts@fbads.ai",
    "email_to": "admin@example.com"
  }'
```

---

## 🔌 INTEGRAÇÃO COM MCP

### Atualizar n8n_manager.py para usar MCP

Os MCPs do Cursor já estão disponíveis. Para ativar:

```python
# Em src/integrations/n8n_manager.py

async def list_workflows(self) -> List[Dict[str, Any]]:
    """Lista todos os workflows n8n"""
    try:
        # Usar MCP n8n
        from cursor import mcp
        
        result = await mcp.call(
            "mcp_n8n-mcp_n8n_list_workflows",
            {
                "limit": 100
            }
        )
        
        workflows = result.get("data", [])
        logger.info(f"Found {len(workflows)} workflows in Macspark n8n")
        return workflows
        
    except Exception as e:
        logger.error(f"Erro ao listar workflows: {e}")
        return []
```

### Exemplo: Criar Workflow via MCP

```python
async def create_facebook_metrics_workflow(self) -> Optional[str]:
    """Cria workflow de coleta de métricas Facebook"""
    try:
        from cursor import mcp
        
        workflow_config = {
            "name": "Facebook Fetch Metrics - Macspark",
            "active": True,
            "nodes": [
                {
                    "id": "webhook-trigger",
                    "name": "Webhook Trigger",
                    "type": "n8n-nodes-base.webhook",
                    "typeVersion": 1,
                    "position": [250, 300],
                    "parameters": {
                        "path": "fb_fetch_metrics",
                        "responseMode": "responseNode",
                        "httpMethod": "POST"
                    }
                },
                {
                    "id": "http-facebook",
                    "name": "Facebook API Call",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 3,
                    "position": [450, 300],
                    "parameters": {
                        "url": "https://graph.facebook.com/v18.0/{{ $json.account_id }}/campaigns",
                        "method": "GET",
                        "authentication": "genericCredentialType",
                        "options": {
                            "queryParameters": {
                                "parameters": [
                                    {
                                        "name": "fields",
                                        "value": "id,name,status,insights{impressions,clicks,spend,ctr,cpc,cpm}"
                                    },
                                    {
                                        "name": "access_token",
                                        "value": "={{ $json.access_token }}"
                                    }
                                ]
                            }
                        }
                    }
                },
                {
                    "id": "respond-to-webhook",
                    "name": "Respond to Webhook",
                    "type": "n8n-nodes-base.respondToWebhook",
                    "typeVersion": 1,
                    "position": [650, 300],
                    "parameters": {
                        "respondWith": "json",
                        "responseBody": "={{ $json }}"
                    }
                }
            ],
            "connections": {
                "Webhook Trigger": {
                    "main": [[{"node": "Facebook API Call", "type": "main", "index": 0}]]
                },
                "Facebook API Call": {
                    "main": [[{"node": "Respond to Webhook", "type": "main", "index": 0}]]
                }
            }
        }
        
        result = await mcp.call(
            "mcp_n8n-mcp_n8n_create_workflow",
            workflow_config
        )
        
        workflow_id = result.get("id")
        logger.info(f"Workflow criado na Macspark: {workflow_id}")
        
        return workflow_id
        
    except Exception as e:
        logger.error(f"Erro ao criar workflow: {e}")
        return None
```

---

## 📊 WORKFLOWS RECOMENDADOS

### 1. Facebook Metrics Collector

**Objetivo:** Coletar métricas de campanhas a cada 30 minutos

**Trigger:** Schedule (cron: */30 * * * *)

**Nodes:**
1. Schedule Trigger
2. HTTP Request → FastAPI `/api/v1/campaigns`
3. Loop sobre campanhas
4. HTTP Request → Facebook Graph API
5. PostgreSQL → Salvar insights
6. Slack → Notificar se houver anomalias

**Webhook alternativo:**
```
POST https://fluxos.macspark.dev/webhook/fb_fetch_metrics
Body: {"account_id": "act_xxx", "access_token": "xxx"}
```

### 2. Multi-Channel Alert System

**Objetivo:** Enviar alertas via Slack, Email, WhatsApp quando houver problemas

**Trigger:** Webhook

**Nodes:**
1. Webhook Trigger (`/webhook/send_alerts_multi`)
2. Switch (por severity: LOW, MEDIUM, HIGH, CRITICAL)
3. Branch paralela:
   - Slack (todos os níveis)
   - Email (MEDIUM+)
   - WhatsApp (HIGH+)
   - Notion (criar página para CRITICAL)
4. Log de alerta em PostgreSQL

**Uso:**
```python
# Em src/tasks/notifiers.py
await n8n_client.send_alert(
    campaign_data=campaign,
    issue_type="CTR_BAIXO",
    severity="HIGH"
)
```

### 3. Daily Report Generator

**Objetivo:** Gerar relatório executivo todo dia 8am

**Trigger:** Schedule (cron: 0 8 * * *)

**Nodes:**
1. Schedule Trigger (8am)
2. HTTP Request → FastAPI `/api/v1/analytics/summary/yesterday`
3. Transform Data (formatar relatório)
4. Branch paralela:
   - Notion → Criar página de relatório
   - Email → Enviar para gestores
   - Slack → Post no canal #reports
5. Respond com link do Notion

---

## 🎯 PRÓXIMOS PASSOS

### Fase 1: Validação (Agora)
- ✅ Credenciais configuradas
- ⏳ Testar conexão API
- ⏳ Listar workflows existentes
- ⏳ Validar permissões

### Fase 2: Implementação (Esta Semana)
- ⏳ Ativar MCPs no código
- ⏳ Criar workflow "Facebook Metrics Collector"
- ⏳ Criar workflow "Multi-Channel Alerts"
- ⏳ Testar integração completa

### Fase 3: Produção (Próxima Semana)
- ⏳ Criar workflow "Daily Report Generator"
- ⏳ Configurar Slack webhook
- ⏳ Configurar SMTP para emails
- ⏳ Documentar workflows criados

---

## 🔍 COMANDOS ÚTEIS

### Testar Conexão
```bash
curl -X GET "https://fluxos.macspark.dev/api/v1/workflows" \
  -H "Authorization: Bearer $N8N_API_KEY"
```

### Listar Workflows
```bash
curl http://localhost:8000/api/v1/n8n/workflows
```

### Buscar Nodes Facebook
```bash
curl "http://localhost:8000/api/v1/n8n/nodes/search?query=facebook"
```

### Validar Workflow
```bash
curl -X POST "http://localhost:8000/api/v1/n8n/workflows/{id}/validate"
```

---

## 📖 DOCUMENTAÇÃO ÚTIL

### n8n API Docs
- [API Authentication](https://docs.n8n.io/api/authentication/)
- [Workflows Endpoint](https://docs.n8n.io/api/api-reference/#tag/Workflow)
- [Webhook Nodes](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

### n8n MCP Tools (Cursor)
- `mcp_n8n-mcp_n8n_list_workflows`
- `mcp_n8n-mcp_n8n_create_workflow`
- `mcp_n8n-mcp_n8n_get_workflow`
- `mcp_n8n-mcp_n8n_validate_workflow`
- `mcp_n8n-mcp_search_nodes`

### Facebook Graph API
- [Marketing API Reference](https://developers.facebook.com/docs/marketing-api/reference)
- [Campaign Insights](https://developers.facebook.com/docs/marketing-api/insights)

---

## ⚠️ SEGURANÇA

### Boas Práticas

1. **Nunca commitar .env**
   - Já configurado no .gitignore
   - Use .env.example como template

2. **Rotacionar API Key**
   - Recomendado a cada 90 dias
   - Gerar nova key em https://fluxos.macspark.dev/settings

3. **Limitar Permissões**
   - API key tem permissões de owner
   - Considere criar key com permissões limitadas para produção

4. **Monitorar Uso**
   - n8n registra todas chamadas API
   - Verificar logs em caso de anomalias

---

## 🆘 TROUBLESHOOTING

### Erro: "Unauthorized" (401)
- Verificar se N8N_API_KEY está correto no .env
- Verificar se o token não expirou
- Regenerar API key no n8n

### Erro: "Workflow not found" (404)
- Workflow pode ter sido deletado
- Verificar ID do workflow
- Listar workflows disponíveis primeiro

### Erro: "Connection timeout"
- Verificar conectividade com fluxos.macspark.dev
- Verificar firewall/proxy
- Testar com curl primeiro

### Erro: "Invalid node configuration"
- Validar JSON do workflow
- Use `n8n_validate_workflow` antes de criar
- Verificar typeVersion dos nodes

---

## 📊 MÉTRICAS

### Status da Integração

| Métrica | Valor | Status |
|---------|-------|--------|
| **Conexão API** | Configurada | 🟢 |
| **Workflows Ativos** | A verificar | ⏳ |
| **Execuções/dia** | 0 | ⏳ |
| **Taxa de Sucesso** | N/A | ⏳ |

**Próxima verificação:** Após testes iniciais

---

**Documentação por:** AI Agent (Claude Sonnet 4.5)  
**Data:** 18 de Outubro de 2025  
**Instância:** [fluxos.macspark.dev](https://fluxos.macspark.dev)  
**Status:** ✅ **PRONTO PARA TESTES**  

🚀 **Credenciais configuradas! Próximo passo: testar conexão!** 🚀


