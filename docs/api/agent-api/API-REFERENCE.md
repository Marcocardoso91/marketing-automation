# 📚 API Reference - Marketing Automation Platform

**Versão:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Última atualização:** 23 de Outubro, 2025

---

## 🔐 Autenticação

### JWT Token
```http
Authorization: Bearer <jwt_token>
```

### API Key (para Analytics)
```http
X-API-Key: <api_key>
```

### Rate Limiting
- **Geral:** 100 requests/minuto
- **Chat:** 30 requests/minuto  
- **Automation:** 10 requests/minuto
- **Metrics Export:** 1000 requests/hora

---

## 🚀 Endpoints Principais

### 🔑 Authentication (`/api/v1/auth`)

#### POST `/api/v1/auth/login`
**Descrição:** Autenticar usuário e obter JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

#### POST `/api/v1/auth/logout`
**Descrição:** Invalidar token JWT

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "message": "Logout successful",
  "timestamp": "2025-10-23T20:59:00Z"
}
```

---

### 📊 Campaigns (`/api/v1/campaigns`)

#### GET `/api/v1/campaigns`
**Descrição:** Listar campanhas do Facebook Ads

**Query Parameters:**
- `status` (optional): `ACTIVE`, `PAUSED`, `ALL`
- `limit` (optional): 1-500 (default: 100)

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": "123456789",
    "name": "Campaign Name",
    "status": "ACTIVE",
    "objective": "CONVERSIONS",
    "created_time": "2025-10-20T10:00:00Z",
    "updated_time": "2025-10-23T15:30:00Z"
  }
]
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/campaigns?status=ACTIVE&limit=50" \
  -H "Authorization: Bearer <token>"
```

#### GET `/api/v1/campaigns/{campaign_id}`
**Descrição:** Obter detalhes de uma campanha específica

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": "123456789",
  "name": "Campaign Name",
  "status": "ACTIVE",
  "objective": "CONVERSIONS",
  "budget": 1000.0,
  "daily_budget": 50.0,
  "created_time": "2025-10-20T10:00:00Z",
  "insights": {
    "impressions": 10000,
    "clicks": 500,
    "spend": 250.0,
    "ctr": 5.0,
    "cpc": 0.50
  }
}
```

---

### 📈 Analytics (`/api/v1/analytics`)

#### GET `/api/v1/analytics/dashboard`
**Descrição:** Obter dados do dashboard principal

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "summary": {
    "total_spend": 5000.0,
    "total_impressions": 100000,
    "total_clicks": 5000,
    "average_ctr": 5.0,
    "average_cpc": 1.0
  },
  "top_campaigns": [
    {
      "id": "123456789",
      "name": "Best Campaign",
      "spend": 1000.0,
      "roas": 4.5
    }
  ],
  "performance_trends": {
    "daily_spend": [100, 150, 200, 180],
    "daily_clicks": [500, 750, 1000, 900]
  }
}
```

---

### 🤖 Automation (`/api/v1/automation`)

#### POST `/api/v1/automation/pause-underperforming`
**Descrição:** Gerar sugestões para pausar campanhas com baixa performance

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "ctr_threshold": 1.0,
  "cpa_threshold": 50.0
}
```

**Response:**
```json
[
  {
    "campaign_id": "123456789",
    "campaign_name": "Low Performance Campaign",
    "current_ctr": 0.5,
    "current_cpa": 75.0,
    "suggestion": "PAUSE",
    "reason": "CTR below threshold (0.5% < 1.0%)"
  }
]
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/automation/pause-underperforming" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"ctr_threshold": 1.0, "cpa_threshold": 50.0}'
```

---

### 💬 Chat (`/api/v1/chat`)

#### POST `/api/v1/chat`
**Descrição:** Interface conversacional para queries em linguagem natural

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "message": "Quais campanhas estão com melhor ROAS?",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "type": "campaigns_list",
  "data": {
    "campaigns": [
      {
        "id": "123456789",
        "name": "Best Campaign",
        "roas": 4.5
      }
    ]
  },
  "message": "Encontrei 3 campanhas com ROAS acima de 3.0"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Quais campanhas estão com melhor ROAS?", "user_id": "user123"}'
```

---

### 📊 Metrics Export (`/api/v1/metrics/export`)

#### GET `/api/v1/metrics/export`
**Descrição:** Exportar métricas formatadas para sistema de analytics

**Headers:** `X-API-Key: <api_key>`

**Query Parameters:**
- `date_from` (required): `YYYY-MM-DD`
- `date_until` (required): `YYYY-MM-DD`

**Response:**
```json
{
  "campaigns": [
    {
      "id": "123456789",
      "name": "Campaign Name",
      "date": "2025-10-23",
      "impressions": 10000,
      "clicks": 500,
      "spend": 250.0,
      "ctr": 5.0,
      "cpc": 0.50,
      "cpm": 25.0
    }
  ],
  "summary": {
    "total_campaigns": 1,
    "total_spend": 250.0,
    "total_impressions": 10000,
    "total_clicks": 500
  },
  "exported_at": "2025-10-23T20:59:00Z"
}
```

**cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-20&date_until=2025-10-23" \
  -H "X-API-Key: <api_key>"
```

---

### 📝 Notion Integration (`/api/v1/notion`)

#### POST `/api/v1/notion/save-campaign-report`
**Descrição:** Salvar relatório de campanha no Notion

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `campaign_id` (required): ID da campanha
- `database_id` (required): ID do database Notion

**Response:**
```json
{
  "success": true,
  "notion_page_id": "page_123456789",
  "notion_url": "https://notion.so/page_123456789",
  "message": "Relatório salvo com sucesso no Notion"
}
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/notion/save-campaign-report?campaign_id=123456789&database_id=db_123456789" \
  -H "Authorization: Bearer <token>"
```

---

### 🔧 N8N Management (`/api/v1/n8n`)

#### GET `/api/v1/n8n/workflows`
**Descrição:** Listar workflows N8N disponíveis

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": "workflow_123",
    "name": "Daily Metrics Collection",
    "status": "active",
    "last_run": "2025-10-23T20:00:00Z",
    "next_run": "2025-10-24T20:00:00Z"
  }
]
```

#### POST `/api/v1/n8n/create-metrics-workflow`
**Descrição:** Criar workflow de coleta de métricas

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "name": "Custom Metrics Workflow",
  "schedule": "0 20 * * *",
  "campaign_ids": ["123456789", "987654321"]
}
```

**Response:**
```json
{
  "success": true,
  "workflow_id": "workflow_456",
  "message": "Workflow criado com sucesso"
}
```

---

## 🚨 Códigos de Erro

### HTTP Status Codes

| Código | Significado | Descrição |
|--------|-------------|-----------|
| `200` | OK | Requisição bem-sucedida |
| `201` | Created | Recurso criado com sucesso |
| `400` | Bad Request | Parâmetros inválidos |
| `401` | Unauthorized | Token inválido ou expirado |
| `403` | Forbidden | Sem permissão para o recurso |
| `404` | Not Found | Recurso não encontrado |
| `422` | Unprocessable Entity | Dados de entrada inválidos |
| `429` | Too Many Requests | Rate limit excedido |
| `500` | Internal Server Error | Erro interno do servidor |

### Error Response Format

```json
{
  "detail": "Error message description",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-10-23T20:59:00Z"
}
```

### Error Codes Específicos

| Código | Descrição | Solução |
|--------|-----------|---------|
| `INVALID_TOKEN` | Token JWT inválido | Renovar token via login |
| `RATE_LIMIT_EXCEEDED` | Rate limit excedido | Aguardar ou usar API key diferente |
| `FACEBOOK_API_ERROR` | Erro na API do Facebook | Verificar credenciais Facebook |
| `SUPABASE_CONNECTION_ERROR` | Erro de conexão Supabase | Verificar URL e chave Supabase |
| `CAMPAIGN_NOT_FOUND` | Campanha não encontrada | Verificar ID da campanha |

---

## 🔄 Webhooks e Callbacks

### N8N Webhook
**URL:** `http://localhost:5678/webhook/metrics-collected`
**Método:** POST
**Payload:**
```json
{
  "event": "metrics_collected",
  "campaign_id": "123456789",
  "date": "2025-10-23",
  "metrics": {
    "impressions": 10000,
    "clicks": 500,
    "spend": 250.0
  }
}
```

---

## 📚 SDKs e Bibliotecas

### Python SDK
```python
from marketing_automation import MarketingAPI

# Inicializar cliente
api = MarketingAPI(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Listar campanhas
campaigns = api.campaigns.list(status="ACTIVE")

# Obter métricas
metrics = api.metrics.export(
    date_from="2025-10-20",
    date_until="2025-10-23"
)
```

### JavaScript SDK
```javascript
import { MarketingAPI } from '@marketing-automation/sdk';

// Inicializar cliente
const api = new MarketingAPI({
  baseUrl: 'http://localhost:8000',
  apiKey: 'your_api_key'
});

// Listar campanhas
const campaigns = await api.campaigns.list({ status: 'ACTIVE' });

// Obter métricas
const metrics = await api.metrics.export({
  dateFrom: '2025-10-20',
  dateUntil: '2025-10-23'
});
```

### cURL Examples
```bash
# Autenticação
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  | jq -r '.access_token')

# Listar campanhas
curl -X GET "http://localhost:8000/api/v1/campaigns" \
  -H "Authorization: Bearer $TOKEN"

# Exportar métricas
curl -X GET "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-20&date_until=2025-10-23" \
  -H "X-API-Key: your_api_key"
```

---

## 🔧 Configuração e Deploy

### Variáveis de Ambiente
```bash
# API Configuration
API_SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret

# Facebook API
FACEBOOK_ACCESS_TOKEN=your_token
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key

# N8N
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_n8n_api_key
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    image: marketing-automation-api:latest
    ports:
      - "8000:8000"
    environment:
      - API_SECRET_KEY=${API_SECRET_KEY}
      - FACEBOOK_ACCESS_TOKEN=${FACEBOOK_ACCESS_TOKEN}
    depends_on:
      - postgres
      - redis
```

---

## 📊 Monitoramento e Métricas

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### Prometheus Metrics
```bash
curl -X GET "http://localhost:8000/metrics"
```

### Logs
```bash
# Ver logs da API
docker-compose logs api

# Filtrar por erro
docker-compose logs api | grep ERROR
```

---

## 🆘 Suporte

### Documentação
- **Guia Completo:** [docs/USER-GUIDE.md](../../USER-GUIDE.md)
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../../reference/troubleshooting/TROUBLESHOOTING.md)
- **Configuração:** [docs/reference/configuration/ENV-VARS.md](../../reference/configuration/ENV-VARS.md)

### Contato
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

**💡 Dica:** Use o Swagger UI em http://localhost:8000/docs para testar os endpoints interativamente!
