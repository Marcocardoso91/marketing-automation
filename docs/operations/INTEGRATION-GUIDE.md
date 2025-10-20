# Guia de Integração - Marketing Automation Platform

> **Status (histórico):** Fluxo documentado em 18/10/2025. Valide endpoints e parâmetros com `README.md` e `RELATORIO-CORRECOES-PENDENTES.md` antes de aplicar em ambientes atuais.

## Visão Geral da Integração

O sistema integrado combina:
- **API (facebook-ads-ai-agent)**: Fonte única de dados Meta Ads, automação inteligente
- **Analytics (Agente Facebook)**: Analytics multi-canal, dashboards, insights IA

### Fluxo de Dados

```
Facebook API
     ↓
Agent API (coleta Meta Ads uma vez)
     ↓
PostgreSQL (agent DB)
     ↓
GET /api/v1/metrics/export
     ↓
Analytics (busca via HTTP)
     ↓
Supabase (data warehouse) ← + GA4, Google Ads, YouTube
     ↓
Apache Superset (dashboards)
     ↓
OpenAI (insights IA)
     ↓
Slack (notificações)
```

## Endpoints de Integração

### GET /api/v1/metrics/export

**Descrição:** Exporta métricas Meta Ads formatadas para o sistema de analytics

**Autenticação:** X-API-Key header

**Rate Limit:** 1000 requests/hora

**Parâmetros:**
- `date_from` (query, obrigatório): Data inicial no formato YYYY-MM-DD
- `date_until` (query, obrigatório): Data final no formato YYYY-MM-DD

**Response:**
```json
{
  "campaigns": [
    {
      "campaign_id": "123",
      "campaign_name": "Campanha Teste",
      "date": "2025-10-18",
      "impressions": 1000,
      "clicks": 50,
      "spend": 100.0,
      "reach": 800,
      "frequency": 1.25,
      "ctr": 5.0,
      "cpc": 2.0,
      "cpe": 1.5,
      "conversions": 10
    }
  ],
  "total_campaigns": 1,
  "date_from": "2025-10-18",
  "date_until": "2025-10-18",
  "exported_at": "2025-10-18T14:30:00Z",
  "data_source": "facebook-ads-ai-agent",
  "version": "1.0.0"
}
```

**Exemplo de uso:**

```bash
curl -H "X-API-Key: your_api_key_here" \
     "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-18&date_until=2025-10-18"
```

## Configuração

### 1. Gerar API Key

```bash
# Windows PowerShell
$key = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "ANALYTICS_API_KEY=$key"
```

### 2. Configurar em ambos .env

**Agent API (.env):**
```bash
ANALYTICS_API_KEY=your_generated_key_here
```

**Analytics (scripts/.env):**
```bash
AGENT_API_URL=http://localhost:8000
# ou em Docker:
# AGENT_API_URL=http://agent-api:8000

ANALYTICS_API_KEY=your_generated_key_here  # Mesma key
```

### 3. Variáveis MCP obrigatórias

As rotas MCP precisam das seguintes variáveis no `.env` do backend:

```bash
# Integração n8n
N8N_API_URL=https://fluxos.macspark.dev/api/v1
N8N_API_KEY=insira_sua_chave_api

# Integração Notion
NOTION_API_TOKEN=secret_xxx
NOTION_DATABASE_ID=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

Sem esses valores, os endpoints `/api/v1/n8n/*` e `/api/v1/notion/*` respondem com **503 Service Unavailable**, indicando que a integração externa ainda não foi configurada.

### 4. Testar Conexão

```python
# test_integration.py
from marketing_shared.utils.api_client import AgentAPIClient

client = AgentAPIClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Health check
print(f"API Health: {client.health_check()}")

# Buscar métricas
metrics = client.get_metrics(
    date_from="2025-10-18",
    date_until="2025-10-18"
)

print(f"Campanhas: {metrics['total_campaigns']}")
```

## Schemas Compartilhados

Os schemas Pydantic garantem que ambos sistemas usam a mesma estrutura de dados:

```python
from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema

# Validação automática
campaign = CampaignMetricSchema(
    campaign_id="123",
    campaign_name="Test",
    date="2025-10-18",
    # ... demais campos
)

# Erros de validação são capturados
# Ex: impressions negativo → ValidationError
```

## Workflow n8n Modificado

O workflow `meta-ads-supabase.json` foi atualizado para buscar do Agent API:

**Antes:**
- Node: Facebook Graph API (OAuth2)
- Busca direto do Facebook

**Depois:**
- Node: HTTP Request
- Busca do Agent API
- Autenticação via X-API-Key
- Retry automático (3x)
- Timeout 30s

## Troubleshooting

### 401 Unauthorized

**Problema:** API key inválida ou ausente

**Solução:**
```bash
# Verificar se keys são iguais
cat api/.env | grep ANALYTICS_API_KEY
cat analytics/scripts/.env | grep ANALYTICS_API_KEY
```

### Connection Refused

**Problema:** Agent API não está rodando

**Solução:**
```bash
# Verificar serviço
docker ps | grep marketing-agent-api

# Iniciar se necessário
docker-compose -f docker-compose.integrated.yml up -d agent-api
```

### Timeout

**Problema:** Request demora mais de 30s

**Solução:**
1. Verificar logs do Agent API
2. Verificar se Facebook API está respondendo
3. Aumentar timeout no cliente:

```python
client = AgentAPIClient(
    base_url="http://localhost:8000",
    api_key="your_key",
    timeout=60  # Aumentar para 60s
)
```

## Monitoramento

### Logs

```bash
# Agent API
docker logs -f marketing-agent-api

# Analytics script
cd analytics/scripts
python metrics-to-supabase.py  # Ver output no console
```

### Métricas

- Total de chamadas à API de exportação
- Erros 401 (autenticação)
- Erros 429 (rate limit)
- Latência média

## Segurança

### Best Practices

✅ API key com mínimo 32 caracteres
✅ Nunca commitar .env no git
✅ Rotar keys periodicamente (3-6 meses)
✅ HTTPS em produção
✅ Rate limiting configurado
✅ Logs de acesso ativados

---

**Atualizado:** 2025-10-18  
**Versão:** 1.0.0

