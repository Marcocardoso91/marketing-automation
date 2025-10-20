# API Specification
## Dashboard Sabrina Costa - REST API

**Versão:** 1.0  
**Base URL (Dev):** `http://localhost:3000/api`  
**Base URL (Prod):** `https://dashboard-sabrina.vercel.app/api`  
**Autenticação:** Bearer Token (JWT)

---

## Índice
1. [Autenticação](#autenticação)
2. [Métricas](#métricas)
3. [Cronograma](#cronograma)
4. [Alertas](#alertas)
5. [Webhook](#webhook)
6. [Configurações](#configurações)
7. [Ganchos](#ganchos)
8. [Códigos de Resposta](#códigos-de-resposta)
9. [Rate Limiting](#rate-limiting)

---

## Autenticação

### POST /api/auth/login
Autenticar usuário e obter token JWT.

**Request:**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "gerente@macspark.dev",
  "password": "senha_segura_123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": "7d",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "gerente@macspark.dev",
    "name": "Marco",
    "role": "admin"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Credenciais inválidas"
}
```

---

### POST /api/auth/logout
Invalidar token atual (opcional, client-side é suficiente).

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout realizado com sucesso"
}
```

---

### GET /api/auth/me
Obter informações do usuário autenticado.

**Request:**
```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "gerente@macspark.dev",
    "name": "Marco",
    "role": "admin",
    "createdAt": "2025-10-20T10:00:00Z"
  }
}
```

---

## Métricas

### GET /api/metrics
Buscar métricas com filtros opcionais.

**Request:**
```http
GET /api/metrics?date=2025-10-20&period=7d
Authorization: Bearer <token>
```

**Query Parameters:**
- `date` (opcional): Data específica (YYYY-MM-DD)
- `period` (opcional): Período em dias (7d, 30d, 90d)
- `startDate` (opcional): Data inicial do intervalo
- `endDate` (opcional): Data final do intervalo
- `limit` (opcional): Número de registros (default: 30)
- `offset` (opcional): Offset para paginação (default: 0)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "date": "2025-10-20",
      "ctr": 6.21,
      "cpc": 0.10,
      "cpm": 2.15,
      "frequency": 1.02,
      "visits": 80,
      "newFollowers": 45,
      "cost": 20.00,
      "impressions": 1091,
      "clicks": 68,
      "costPerFollower": 0.44,
      "createdAt": "2025-10-20T18:00:00Z"
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "date": "2025-10-19",
      "ctr": 5.85,
      "cpc": 0.12,
      "cpm": 2.30,
      "frequency": 1.15,
      "visits": 75,
      "newFollowers": 40,
      "cost": 20.00,
      "impressions": 1050,
      "clicks": 61,
      "costPerFollower": 0.50,
      "createdAt": "2025-10-19T18:00:00Z"
    }
  ],
  "pagination": {
    "total": 30,
    "limit": 30,
    "offset": 0,
    "hasMore": false
  }
}
```

---

### POST /api/metrics
Criar nova métrica (manual).

**Request:**
```http
POST /api/metrics
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2025-10-21",
  "ctr": 7.5,
  "cpc": 0.09,
  "cpm": 2.0,
  "frequency": 0.98,
  "visits": 90,
  "newFollowers": 50,
  "cost": 20.00,
  "impressions": 1200,
  "clicks": 90
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "date": "2025-10-21",
    "ctr": 7.5,
    "cpc": 0.09,
    "cpm": 2.0,
    "frequency": 0.98,
    "visits": 90,
    "newFollowers": 50,
    "cost": 20.00,
    "impressions": 1200,
    "clicks": 90,
    "costPerFollower": 0.40,
    "createdAt": "2025-10-21T18:00:00Z"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Validação falhou",
  "details": {
    "date": "Data não pode ser futura",
    "ctr": "CTR deve estar entre 0 e 100"
  }
}
```

**Response (409 Conflict):**
```json
{
  "success": false,
  "error": "Métrica para esta data já existe"
}
```

---

### PUT /api/metrics/:id
Atualizar métrica existente.

**Request:**
```http
PUT /api/metrics/323e4567-e89b-12d3-a456-426614174002
Authorization: Bearer <token>
Content-Type: application/json

{
  "ctr": 8.0,
  "newFollowers": 55
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "date": "2025-10-21",
    "ctr": 8.0,
    "cpc": 0.09,
    "cpm": 2.0,
    "frequency": 0.98,
    "visits": 90,
    "newFollowers": 55,
    "cost": 20.00,
    "impressions": 1200,
    "clicks": 96,
    "costPerFollower": 0.36,
    "updatedAt": "2025-10-21T19:00:00Z"
  }
}
```

---

### DELETE /api/metrics/:id
Deletar métrica (apenas admin).

**Request:**
```http
DELETE /api/metrics/323e4567-e89b-12d3-a456-426614174002
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Métrica deletada com sucesso"
}
```

---

### GET /api/metrics/summary
Obter resumo estatístico.

**Request:**
```http
GET /api/metrics/summary?period=30d
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "period": "30d",
    "totalDays": 30,
    "averages": {
      "ctr": 5.8,
      "cpc": 0.11,
      "cpm": 2.25,
      "frequency": 1.05,
      "visitsPerDay": 78,
      "newFollowersPerDay": 43,
      "costPerDay": 20.00
    },
    "totals": {
      "visits": 2340,
      "newFollowers": 1290,
      "cost": 600.00,
      "costPerFollower": 0.47
    },
    "trends": {
      "ctr": "+12.5%",
      "newFollowers": "+8.3%",
      "cost": "0%"
    }
  }
}
```

---

## Cronograma

### GET /api/schedule
Buscar posts do cronograma.

**Request:**
```http
GET /api/schedule?week=1&status=planned
Authorization: Bearer <token>
```

**Query Parameters:**
- `week` (opcional): Número da semana (1, 2, 3, 4)
- `status` (opcional): Status do post (planned, posted, cancelled)
- `date` (opcional): Data específica (YYYY-MM-DD)
- `format` (opcional): Formato do post (reel, carousel, stories)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "423e4567-e89b-12d3-a456-426614174003",
      "date": "2025-10-21",
      "weekNumber": 1,
      "format": "reel",
      "theme": "Transformação Antes/Depois",
      "hook": "Olha só o que 7 dias fizeram...",
      "cta": "Me segue pra ver mais transformações",
      "objective": "Migração Tráfego + Seguidores",
      "storiesIdeas": "3-5 stories: Bastidores da gravação + Enquete",
      "status": "planned",
      "postedAt": null,
      "createdAt": "2025-10-20T10:00:00Z"
    },
    {
      "id": "523e4567-e89b-12d3-a456-426614174004",
      "date": "2025-10-23",
      "weekNumber": 1,
      "format": "reel",
      "theme": "Autocuidado Real",
      "hook": "Hoje escolhi ME CUIDAR...",
      "cta": "Salva pra lembrar",
      "objective": "Salvamentos + Alcance",
      "storiesIdeas": "Behind the scenes do Reel + Caixinha de perguntas",
      "status": "planned",
      "postedAt": null,
      "createdAt": "2025-10-20T10:00:00Z"
    }
  ],
  "count": 2
}
```

---

### PUT /api/schedule/:id
Atualizar status do post.

**Request:**
```http
PUT /api/schedule/423e4567-e89b-12d3-a456-426614174003
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "posted"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "date": "2025-10-21",
    "format": "reel",
    "theme": "Transformação Antes/Depois",
    "status": "posted",
    "postedAt": "2025-10-21T18:30:00Z",
    "updatedAt": "2025-10-21T18:30:00Z"
  }
}
```

---

### POST /api/schedule
Criar um novo item no cronograma (apenas admin).

**Request:**
```http
POST /api/schedule
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "2025-10-24",
  "weekNumber": 2,
  "format": "carousel",
  "theme": "Checklist de Stories",
  "hook": "Você esquece desses 3 passos?",
  "cta": "Salva pra revisar depois",
  "objective": "Engajamento",
  "storiesIdeas": "Bastidores + enquete + CTA"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "623e4567-e89b-12d3-a456-426614174070",
    "date": "2025-10-24",
    "weekNumber": 2,
    "format": "carousel",
    "theme": "Checklist de Stories",
    "status": "planned",
    "createdAt": "2025-10-20T15:00:00Z"
  }
}
```

---

## Alertas

### GET /api/alerts
Listar alertas.

**Request:**
```http
GET /api/alerts?limit=10&status=sent
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (opcional): Número de alertas (default: 10)
- `offset` (opcional): Offset para paginação
- `status` (opcional): Status (sent, pending, failed)
- `type` (opcional): Tipo de alerta (ctr_low, cpc_high, etc)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "623e4567-e89b-12d3-a456-426614174005",
      "type": "ctr_low",
      "message": "⚠️ ALERTA: CTR abaixo da meta (1.2% < 1.5%)",
      "sentAt": "2025-10-20T18:05:00Z",
      "status": "sent",
      "metadata": {
        "date": "2025-10-20",
        "ctr": 1.2,
        "threshold": 1.5
      }
    },
    {
      "id": "723e4567-e89b-12d3-a456-426614174006",
      "type": "cpc_high",
      "message": "⚠️ ALERTA: CPC acima da meta (R$0.75 > R$0.70)",
      "sentAt": "2025-10-19T18:05:00Z",
      "status": "sent",
      "metadata": {
        "date": "2025-10-19",
        "cpc": 0.75,
        "threshold": 0.70
      }
    }
  ],
  "pagination": {
    "total": 15,
    "limit": 10,
    "offset": 0,
    "hasMore": true
  }
}
```

---

### POST /api/alerts
Criar novo alerta (usado por n8n).

**Request:**
```http
POST /api/alerts
Authorization: Bearer <token>
Content-Type: application/json

{
  "type": "frequency_high",
  "message": "⚠️ ALERTA: Frequência muito alta (3.5 > 3.0)",
  "metadata": {
    "date": "2025-10-21",
    "frequency": 3.5,
    "threshold": 3.0
  }
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "823e4567-e89b-12d3-a456-426614174007",
    "type": "frequency_high",
    "message": "⚠️ ALERTA: Frequência muito alta (3.5 > 3.0)",
    "sentAt": "2025-10-21T18:05:00Z",
    "status": "sent",
    "metadata": {
      "date": "2025-10-21",
      "frequency": 3.5,
      "threshold": 3.0
    }
  }
}
```

---

### PUT /api/alerts/config
Atualizar configurações de alertas.

**Request:**
```http
PUT /api/alerts/config
Authorization: Bearer <token>
Content-Type: application/json

{
  "thresholds": {
    "ctrMin": 1.5,
    "cpcMax": 0.70,
    "cpmMax": 10.0,
    "frequencyMax": 3.0,
    "costPerFollowerMax": 1.30
  },
  "whatsapp": {
    "number": "+5511999999999",
    "enabled": true
  },
  "schedule": {
    "dailyReport": "18:00",
    "postReminders": ["11:00", "17:30"]
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Configurações atualizadas com sucesso",
  "data": {
    "thresholds": {
      "ctrMin": 1.5,
      "cpcMax": 0.70,
      "cpmMax": 10.0,
      "frequencyMax": 3.0,
      "costPerFollowerMax": 1.30
    },
    "whatsapp": {
      "number": "+5511999999999",
      "enabled": true
    },
    "schedule": {
      "dailyReport": "18:00",
      "postReminders": ["11:00", "17:30"]
    },
    "updatedAt": "2025-10-21T19:00:00Z"
  }
}
```

---

### GET /api/alerts/config
Obter configurações atuais.

**Request:**
```http
GET /api/alerts/config
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "thresholds": {
      "ctrMin": 1.5,
      "cpcMax": 0.70,
      "cpmMax": 10.0,
      "frequencyMax": 3.0,
      "costPerFollowerMax": 1.30
    },
    "whatsapp": {
      "number": "+5511999999999",
      "enabled": true
    },
    "schedule": {
      "dailyReport": "18:00",
      "postReminders": ["11:00", "17:30"]
    }
  }
}
```

---

## Webhook

### POST /api/webhook/metrics
Receber métricas do n8n (autenticação via header especial).

**Request:**
```http
POST /api/webhook/metrics
X-Webhook-Token: secret_webhook_token_here
Content-Type: application/json

{
  "date": "2025-10-21",
  "ctr": 7.5,
  "cpc": 0.09,
  "cpm": 2.0,
  "frequency": 0.98,
  "visits": 90,
  "newFollowers": 50,
  "cost": 20.00,
  "impressions": 1200,
  "clicks": 90
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Métrica recebida e processada",
  "savedRecords": 1,
  "alertsGenerated": 0,
  "data": {
    "id": "923e4567-e89b-12d3-a456-426614174008",
    "date": "2025-10-21",
    "costPerFollower": 0.40
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Token de webhook inválido"
}
```

---

### POST /api/webhook/metrics/csv
Receber CSV de métricas (parsing automático).

**Request:**
```http
POST /api/webhook/metrics/csv
X-Webhook-Token: secret_webhook_token_here
Content-Type: text/csv

date,ctr,cpc,cpm,frequency,visits,newFollowers,cost,impressions,clicks
2025-10-21,7.5,0.09,2.0,0.98,90,50,20.00,1200,90
2025-10-22,8.0,0.08,1.9,0.95,95,55,20.00,1250,100
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "CSV processado com sucesso",
  "savedRecords": 2,
  "alertsGenerated": 0,
  "errors": []
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Erro ao processar CSV",
  "details": [
    {
      "row": 2,
      "error": "CTR inválido: deve ser número entre 0 e 100"
    }
  ]
}
```

---

## Configurações

### GET /api/config
Obter todas configurações.

**Request:**
```http
GET /api/config
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "thresholds": {
      "ctrMin": 1.5,
      "cpcMax": 0.70,
      "cpmMax": 10.0,
      "frequencyMax": 3.0,
      "costPerFollowerMax": 1.30
    },
    "whatsapp": {
      "number": "+5511999999999",
      "enabled": true
    },
    "schedule": {
      "dailyReport": "18:00",
      "postReminders": ["11:00", "17:30"]
    },
    "general": {
      "timezone": "America/Sao_Paulo",
      "currency": "BRL",
      "language": "pt-BR"
    }
  }
}
```

---

### GET /api/config/:key
Obter uma chave específica (`thresholds`, `whatsapp`, `alertsSchedule`, `general`).

**Request:**
```http
GET /api/config/thresholds
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "ctrMin": 1.5,
    "cpcMax": 0.70,
    "cpmMax": 10.0,
    "frequencyMax": 3.0,
    "costPerFollowerMax": 1.30
  }
}
```

---

### PUT /api/config
Atualizar múltiplas configurações (apenas admin).

**Request:**
```http
PUT /api/config
Authorization: Bearer <token>
Content-Type: application/json

{
  "thresholds": {
    "ctrMin": 1.6,
    "cpcMax": 0.65
  },
  "general": {
    "timezone": "America/Sao_Paulo",
    "currency": "BRL",
    "language": "pt-BR"
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Configurações atualizadas com sucesso",
  "data": {
    "thresholds": {
      "ctrMin": 1.6,
      "cpcMax": 0.65,
      "cpmMax": 10.0,
      "frequencyMax": 3.0,
      "costPerFollowerMax": 1.30
    },
    "whatsapp": {
      "number": "+5511999999999",
      "enabled": true
    },
    "alertsSchedule": {
      "dailyReport": "18:00",
      "postReminders": ["11:00", "17:30"]
    },
    "general": {
      "timezone": "America/Sao_Paulo",
      "currency": "BRL",
      "language": "pt-BR"
    }
  }
}
```

---

## Ganchos

### GET /api/hooks
Listar ganchos virais.

**Request:**
```http
GET /api/hooks?category=Curiosidade
Authorization: Bearer <token>
```

**Query Parameters:**
- `category` (opcional): Filtrar por categoria
- `search` (opcional): Buscar por palavra-chave
- `limit` (opcional): Número de resultados (default: 50)

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "a23e4567-e89b-12d3-a456-426614174009",
      "category": "Curiosidade",
      "text": "O que NINGUÉM te conta sobre...",
      "usageCount": 5
    },
    {
      "id": "b23e4567-e89b-12d3-a456-426614174010",
      "category": "Curiosidade",
      "text": "Esse segredo mudou TUDO para mim",
      "usageCount": 3
    }
  ],
  "count": 2,
  "categories": [
    "Curiosidade",
    "Urgência",
    "Transformação",
    "Identificação",
    "Lista/Número",
    "Desafio",
    "Comparação",
    "História",
    "Pergunta",
    "Autoridade"
  ]
}
```

---

### PUT /api/hooks/:id/increment
Incrementar contador de uso (quando copiado).

**Request:**
```http
PUT /api/hooks/a23e4567-e89b-12d3-a456-426614174009/increment
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "a23e4567-e89b-12d3-a456-426614174009",
    "usageCount": 6
  }
}
```

---

### GET /api/hooks/categories/list
Listar categorias disponíveis (para filtros do frontend).

**Request:**
```http
GET /api/hooks/categories/list
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    "Curiosidade",
    "Urgência",
    "Transformação",
    "Identificação",
    "Lista/Número",
    "Desafio",
    "Comparação",
    "História",
    "Pergunta",
    "Autoridade"
  ]
}
```

---

## Códigos de Resposta

| Código | Status | Descrição |
|--------|--------|-----------|
| 200 | OK | Requisição bem-sucedida |
| 201 | Created | Recurso criado com sucesso |
| 400 | Bad Request | Erro de validação ou dados inválidos |
| 401 | Unauthorized | Token ausente ou inválido |
| 403 | Forbidden | Sem permissão para acessar recurso |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Conflito (ex: registro duplicado) |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Erro interno do servidor |

---

## Rate Limiting

### Limites Gerais
- **Autenticação**: 10 tentativas/minuto por IP
- **API Geral**: 100 requisições/minuto por token
- **Webhook**: 60 requisições/minuto por token

### Headers de Rate Limit
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1634567890
```

### Response quando excedido (429)
```json
{
  "success": false,
  "error": "Rate limit excedido",
  "retryAfter": 60,
  "message": "Aguarde 60 segundos antes de tentar novamente"
}
```

---

## Paginação

Endpoints que retornam listas suportam paginação:

**Query Parameters:**
- `limit`: Número de itens por página (default: 10, max: 100)
- `offset`: Número de itens a pular (default: 0)

**Response Pattern:**
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 150,
    "limit": 10,
    "offset": 0,
    "hasMore": true,
    "nextOffset": 10
  }
}
```

---

## Versionamento

A API não usa versionamento em URL nesta versão inicial. Mudanças breaking serão comunicadas com antecedência.

Futuramente:
- `/api/v1/metrics`
- `/api/v2/metrics`

---

## Exemplos de Uso

### Exemplo 1: Fluxo Completo de Login e Busca de Métricas

```javascript
// 1. Login
const loginResponse = await fetch('https://dashboard-sabrina.vercel.app/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'gerente@macspark.dev',
    password: 'senha_segura_123'
  })
});

const { token } = await loginResponse.json();

// 2. Buscar métricas dos últimos 7 dias
const metricsResponse = await fetch('https://dashboard-sabrina.vercel.app/api/metrics?period=7d', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const { data: metrics } = await metricsResponse.json();
console.log(metrics);
```

### Exemplo 2: n8n Enviando Métricas via Webhook

```javascript
// No n8n (HTTP Request Node)
const response = await fetch('https://dashboard-sabrina.vercel.app/api/webhook/metrics', {
  method: 'POST',
  headers: {
    'X-Webhook-Token': 'secret_webhook_token_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    date: '2025-10-21',
    ctr: 7.5,
    cpc: 0.09,
    cpm: 2.0,
    frequency: 0.98,
    visits: 90,
    newFollowers: 50,
    cost: 20.00,
    impressions: 1200,
    clicks: 90
  })
});
```

---

**Documento vivo**: Esta especificação será atualizada conforme novos endpoints forem adicionados.

