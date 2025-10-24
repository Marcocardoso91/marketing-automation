# 📝 Guia Notion - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🎯 O Que É Notion Integration

A **integração Notion** permite salvar relatórios, dashboards e análises automaticamente no Notion, criando um hub centralizado de informações de marketing. Funcionalidades:

- ✅ **Relatórios automáticos** de campanhas
- ✅ **Dashboards** em tempo real
- ✅ **Sumários diários** executivos
- ✅ **Templates** personalizáveis
- ✅ **Automação** via N8N
- ✅ **Colaboração** em equipe

---

## 📋 Pré-requisitos

### Conta Notion
- ✅ Workspace Notion ativo
- ✅ Permissões de administrador
- ✅ Database criado para relatórios

### Credenciais
- **Notion API Token** (Integration Token)
- **Database ID** do workspace
- **Agent API Key** (para endpoints)

### Configuração Notion
1. **Notion → Settings & Members → Connections**
2. **New integration** → Nome: "Marketing Automation"
3. **Copy Integration Token** (começa com `secret_`)
4. **Share database** com a integration

---

## 🔧 Configuração Inicial

### 1. Obter Notion API Token

#### Passo 1: Criar Integration
1. **Acessar:** https://www.notion.so/my-integrations
2. **Clicar:** "New integration"
3. **Preencher:**
   - **Name:** `Marketing Automation Platform`
   - **Logo:** Upload logo (opcional)
   - **Associated workspace:** Selecionar workspace
4. **Clicar:** "Submit"
5. **Copiar:** "Internal Integration Token"

#### Passo 2: Compartilhar Database
1. **Abrir database** no Notion
2. **Clicar:** "Share" (canto superior direito)
3. **Adicionar:** Nome da integration criada
4. **Selecionar:** "Can edit" ou "Can read"
5. **Clicar:** "Invite"

#### Passo 3: Obter Database ID
1. **Abrir database** no Notion
2. **URL:** `https://notion.so/workspace/DATABASE_ID?v=...`
3. **Copiar:** `DATABASE_ID` (32 caracteres)

### 2. Configurar Variáveis de Ambiente

```bash
# Adicionar ao .env
NOTION_API_KEY=secret_your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

### 3. Testar Conexão

```bash
# Testar API Notion
curl -X GET "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

**Response esperado:**
```json
{
  "object": "user",
  "id": "user_id",
  "name": "Your Name",
  "avatar_url": null,
  "type": "person"
}
```

---

## 🗄️ Estrutura do Database

### Schema Recomendado

**Propriedades do Database:**
```json
{
  "Campaign ID": {
    "type": "title",
    "title": {}
  },
  "Campaign Name": {
    "type": "rich_text",
    "rich_text": {}
  },
  "Date": {
    "type": "date",
    "date": {}
  },
  "Status": {
    "type": "select",
    "select": {
      "options": [
        {"name": "Active", "color": "green"},
        {"name": "Paused", "color": "yellow"},
        {"name": "Completed", "color": "blue"}
      ]
    }
  },
  "Spend": {
    "type": "number",
    "number": {
      "format": "currency",
      "currency_code": "BRL"
    }
  },
  "CTR": {
    "type": "number",
    "number": {
      "format": "percent"
    }
  },
  "ROAS": {
    "type": "number",
    "number": {
      "format": "number"
    }
  },
  "Performance Score": {
    "type": "number",
    "number": {
      "format": "number"
    }
  },
  "Tags": {
    "type": "multi_select",
    "multi_select": {
      "options": [
        {"name": "High Performance", "color": "green"},
        {"name": "Needs Optimization", "color": "yellow"},
        {"name": "Underperforming", "color": "red"}
      ]
    }
  }
}
```

### Templates de Páginas

#### Template 1: Relatório de Campanha
```markdown
# 📊 Relatório de Campanha: {{campaign_name}}

**Campaign ID:** {{campaign_id}}  
**Data:** {{date}}  
**Status:** {{status}}

## 📈 Métricas Principais

| Métrica | Valor | Status |
|---------|-------|--------|
| **Spend** | R$ {{spend}} | {{spend_status}} |
| **CTR** | {{ctr}}% | {{ctr_status}} |
| **CPC** | R$ {{cpc}} | {{cpc_status}} |
| **ROAS** | {{roas}}x | {{roas_status}} |

## 🎯 Performance Score

**Score:** {{performance_score}}/100
**Rating:** {{rating_visual}}

## 💡 Sugestões de Otimização

{{suggestions}}

## 📊 Gráficos

{{charts_placeholder}}
```

#### Template 2: Sumário Diário
```markdown
# 📅 Sumário Diário - {{date}}

## 💰 Resumo Financeiro

- **Gasto Total:** R$ {{total_spend}}
- **Campanhas Ativas:** {{active_campaigns}}
- **Novas Campanhas:** {{new_campaigns}}

## 🏆 Top 5 Performers

{{top_performers_table}}

## ⚠️ Campanhas Problemáticas

{{underperformers_table}}

## 📈 Insights do Dia

{{insights}}
```

---

## 🚀 Endpoints da API

### 1. Salvar Relatório de Campanha

#### POST `/api/v1/notion/save-campaign-report`

**Descrição:** Salva relatório detalhado de uma campanha específica

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `campaign_id` (required): ID da campanha
- `database_id` (required): ID do database Notion

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/notion/save-campaign-report?campaign_id=123456789&database_id=abc123def456" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "notion_page_id": "page_123456789",
  "notion_url": "https://notion.so/page_123456789",
  "message": "Relatório salvo com sucesso no Notion",
  "campaign_data": {
    "id": "123456789",
    "name": "Campaign Name",
    "spend": 250.0,
    "ctr": 5.2,
    "roas": 3.8
  }
}
```

### 2. Criar Sumário Diário

#### POST `/api/v1/notion/daily-summary`

**Descrição:** Cria sumário executivo de todas as campanhas do dia

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `database_id` (required): ID do database Notion
- `date` (optional): Data no formato YYYY-MM-DD (default: ontem)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/notion/daily-summary?database_id=abc123def456&date=2025-10-23" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "notion_page_id": "page_987654321",
  "notion_url": "https://notion.so/page_987654321",
  "summary_data": {
    "total_spend": 1500.0,
    "active_campaigns": 5,
    "top_performers": [
      {
        "id": "123456789",
        "name": "Best Campaign",
        "roas": 4.5
      }
    ]
  }
}
```

### 3. Buscar Relatórios

#### GET `/api/v1/notion/reports`

**Descrição:** Lista relatórios salvos no Notion

**Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Query Parameters:**
- `database_id` (required): ID do database Notion
- `limit` (optional): Número máximo de resultados (default: 10)
- `filter` (optional): Filtrar por status, tags, etc.

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/notion/reports?database_id=abc123def456&limit=5" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "reports": [
    {
      "notion_page_id": "page_123456789",
      "notion_url": "https://notion.so/page_123456789",
      "campaign_id": "123456789",
      "campaign_name": "Campaign Name",
      "date": "2025-10-23",
      "performance_score": 85
    }
  ],
  "total_count": 15
}
```

---

## 🤖 Automação com N8N

### Workflow 1: Relatório Diário Automático

**Configuração N8N:**
```json
{
  "name": "Daily Notion Report",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]
        }
      }
    },
    {
      "name": "Create Daily Summary",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/notion/daily-summary",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}",
          "Content-Type": "application/json"
        },
        "qs": {
          "database_id": "{{$credentials.notion.databaseId}}"
        }
      }
    },
    {
      "name": "Send Notification",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#marketing-reports",
        "text": "📊 Relatório diário criado: {{$json.notion_url}}"
      }
    }
  ]
}
```

### Workflow 2: Relatório de Campanha

**Configuração N8N:**
```json
{
  "name": "Campaign Report to Notion",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "campaign-report",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Save Campaign Report",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/notion/save-campaign-report",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}"
        },
        "qs": {
          "campaign_id": "={{$json.campaign_id}}",
          "database_id": "{{$credentials.notion.databaseId}}"
        }
      }
    }
  ]
}
```

### Workflow 3: Alerta de Performance

**Configuração N8N:**
```json
{
  "name": "Performance Alert to Notion",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "cronExpression", "expression": "0 */4 * * *"}]
        }
      }
    },
    {
      "name": "Check Performance",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "GET",
        "url": "http://localhost:8000/api/v1/analytics/dashboard",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}"
        }
      }
    },
    {
      "name": "IF Performance Check",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$json.summary.average_ctr}}",
              "operation": "smaller",
              "value2": 1.0
            }
          ]
        }
      }
    },
    {
      "name": "Create Alert Report",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/notion/daily-summary",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}"
        },
        "qs": {
          "database_id": "{{$credentials.notion.databaseId}}"
        }
      }
    }
  ]
}
```

---

## 📊 Exemplos Práticos

### Exemplo 1: Relatório Manual via API

```python
import requests

# Configuração
api_url = "http://localhost:8000"
jwt_token = "your_jwt_token"
database_id = "your_database_id"
campaign_id = "123456789"

# Salvar relatório de campanha
response = requests.post(
    f"{api_url}/api/v1/notion/save-campaign-report",
    headers={"Authorization": f"Bearer {jwt_token}"},
    params={
        "campaign_id": campaign_id,
        "database_id": database_id
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Relatório salvo: {data['notion_url']}")
else:
    print(f"❌ Erro: {response.text}")
```

### Exemplo 2: Sumário Diário Automático

```bash
#!/bin/bash
# Script para criar sumário diário

API_URL="http://localhost:8000"
JWT_TOKEN="your_jwt_token"
DATABASE_ID="your_database_id"

# Criar sumário do dia anterior
curl -X POST "${API_URL}/api/v1/notion/daily-summary" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"database_id\": \"${DATABASE_ID}\", \"date\": \"$(date -d 'yesterday' +%Y-%m-%d)\"}"
```

### Exemplo 3: Integração com Slack

```json
{
  "name": "Notion Report + Slack",
  "nodes": [
    {
      "name": "Create Notion Report",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/api/v1/notion/daily-summary",
        "headers": {
          "Authorization": "Bearer {{$credentials.agentApi.jwtToken}}"
        }
      }
    },
    {
      "name": "Send to Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#marketing",
        "text": "📊 Relatório diário criado no Notion: {{$json.notion_url}}"
      }
    }
  ]
}
```

---

## 🚨 Troubleshooting

### Problemas Comuns

#### ❌ Notion API Error 401
**Sintomas:** `Unauthorized` ou `Invalid token`

**Soluções:**
1. **Verificar token** Notion válido
2. **Verificar permissões** da integration
3. **Renovar token** se necessário
4. **Verificar workspace** correto

#### ❌ Database Not Found
**Sintomas:** `Object not found` ou `Database ID invalid`

**Soluções:**
1. **Verificar Database ID** correto
2. **Compartilhar database** com integration
3. **Verificar permissões** de acesso
4. **Testar conexão** manualmente

#### ❌ Rate Limit Exceeded
**Sintomas:** `Rate limit exceeded` ou `Too many requests`

**Soluções:**
1. **Reduzir frequência** de requests
2. **Implementar delays** entre chamadas
3. **Usar batch operations** quando possível
4. **Monitorar rate limits** da API

#### ❌ Dados Não Aparecem
**Sintomas:** API retorna sucesso mas dados não chegam

**Soluções:**
1. **Verificar schema** do database
2. **Verificar mapeamento** de campos
3. **Testar com dados simples**
4. **Verificar logs** da API

### Debugging

#### Verificar Conexão Notion
```bash
# Testar API Notion diretamente
curl -X GET "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

#### Verificar Database
```bash
# Testar acesso ao database
curl -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 1}'
```

#### Verificar Logs da API
```bash
# Ver logs da API
docker-compose logs api | grep -i notion
```

---

## 📈 Monitoramento e Otimização

### Métricas Importantes

- **Taxa de sucesso** dos relatórios
- **Tempo de criação** das páginas
- **Erros por tipo** de operação
- **Rate limits** da API Notion

### Otimizações

1. **Batch operations** para múltiplas campanhas
2. **Templates reutilizáveis** para relatórios
3. **Cache** de dados frequentes
4. **Retry logic** para erros temporários

### Alertas de Sistema

1. **API Notion** indisponível
2. **Rate limit** excedido
3. **Database** não acessível
4. **Token** expirado

---

## 🔗 Recursos Adicionais

### Documentação
- **Notion API:** https://developers.notion.com
- **API Reference:** [docs/api/agent-api/API-REFERENCE.md](../agent-api/API-REFERENCE.md)
- **N8N Guide:** [docs/api/integrations/N8N-GUIDE.md](./N8N-GUIDE.md)

### Templates
- **Notion Templates:** [analytics/notion-pages/](../../../analytics/notion-pages/)
- **Database Schema:** Ver seção "Estrutura do Database"
- **Page Templates:** Ver seção "Templates de Páginas"

### Suporte
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../../reference/troubleshooting/TROUBLESHOOTING.md)
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)

---

## ✅ Checklist de Configuração

### Configuração Básica
- [ ] ✅ Conta Notion ativa
- [ ] ✅ Integration criada
- [ ] ✅ Database configurado
- [ ] ✅ Permissões corretas
- [ ] ✅ API token válido
- [ ] ✅ Database ID correto

### Configuração Avançada
- [ ] ✅ Templates personalizados
- [ ] ✅ Workflows N8N configurados
- [ ] ✅ Automação funcionando
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Backup dos templates
- [ ] ✅ Documentação da equipe

---

**💡 Dica:** Comece com relatórios simples e vá adicionando complexidade gradualmente!
