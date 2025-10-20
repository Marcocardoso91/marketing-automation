# PRD - Agent API (facebook-ads-ai-agent)

**Versão:** 1.0.0
**Data:** 18 de Outubro, 2025
**Status (histórico):** Documento de 18/10/2025. Consulte a documentação atualizada (`README.md`, `RELATORIO-CORRECOES-PENDENTES.md`) para o estado mais recente.
**Owner:** Marco @ Macspark
**Repositório:** `marketing-automation/api/`

---

## 1. Visão e Objetivos

### 1.1 Visão do Produto

O **Agent API** é uma API REST inteligente para automação e otimização de campanhas Meta Ads, oferecendo:
- 📊 Coleta e análise automatizada de métricas
- 🤖 Chat IA para consultas em linguagem natural
- 💡 Sugestões automáticas de otimização baseadas em ML
- 🔄 Automação de regras (pause/ative campanhas)
- 📈 Relatórios agendados e webhooks
- 🔌 Exportação de métricas para sistemas externos

### 1.2 Objetivos Principais

- ✅ Centralizar gestão de Meta Ads em API profissional
- ✅ Automatizar 80% das tarefas repetitivas
- ✅ Melhorar ROI através de otimizações baseadas em dados
- ✅ Fornecer fonte única de dados Meta Ads para outros sistemas
- ✅ Escalar para suportar 10+ contas simultaneamente

---

## 2. Funcionalidades

### 2.1 Autenticação e Usuários

| Feature | Descrição | Status |
|---------|-----------|--------|
| **JWT Authentication** | Login com email/password retorna token JWT | ✅ |
| **Token Refresh** | Renovação de tokens expirados | ✅ |
| **Múltiplos Usuários** | Suporte a diferentes níveis de acesso | ✅ |
| **Audit Logs** | Registro de todas as ações de usuários | ✅ |

**Endpoints:**
- `POST /api/v1/auth/login` - Fazer login
- `POST /api/v1/auth/refresh` - Renovar token
- `GET /api/v1/users/me` - Perfil do usuário

---

### 2.2 Gestão de Campanhas

| Feature | Descrição | Status |
|---------|-----------|--------|
| **Listar Campanhas** | GET com filtros (status, data, ad_account) | ✅ |
| **Detalhes de Campanha** | Métricas completas de uma campanha específica | ✅ |
| **Insights Históricos** | Dados agregados por período | ✅ |
| **Sync Manual** | Forçar coleta de dados do Facebook | ✅ |

**Endpoints:**
- `GET /api/v1/campaigns/` - Listar campanhas
- `GET /api/v1/campaigns/{id}` - Detalhe de campanha
- `GET /api/v1/campaigns/{id}/insights` - Insights históricos
- `POST /api/v1/campaigns/sync` - Sincronizar com Facebook

---

### 2.3 Chat IA

| Feature | Descrição | Status |
|---------|-----------|--------|
| **Perguntas Naturais** | "Quais campanhas têm melhor ROI?" | ✅ |
| **Contexto Persistente** | Conversa com histórico | ✅ |
| **Sugestões Proativas** | "Campanha X está abaixo da meta" | ✅ |
| **Multilíngue** | PT-BR e EN-US | ✅ |

**Endpoints:**
- `POST /api/v1/chat` - Enviar mensagem
- `GET /api/v1/chat/history` - Histórico de conversas

**Exemplo:**
```json
POST /api/v1/chat
{
  "message": "Quais campanhas têm CTR acima de 5%?"
}

Response:
{
  "response": "Encontrei 3 campanhas com CTR > 5%: Campanha A (6.2%), Campanha B (5.8%), Campanha C (5.3%). A Campanha A tem o melhor desempenho com CPC de R$ 0.45.",
  "campaigns": [...],
  "suggestions": ["Considere aumentar budget da Campanha A"]
}
```

---

### 2.4 Sugestões Automáticas

| Feature | Descrição | Status |
|---------|-----------|--------|
| **Budget Optimization** | Sugere realocação de budget | ✅ |
| **Pause Low Performers** | Identifica campanhas de baixo ROI | ✅ |
| **Creative Refresh** | Detecta fadiga de anúncios | ✅ |
| **Audience Expansion** | Sugere novos públicos similares | ✅ |

**Endpoints:**
- `GET /api/v1/suggestions/` - Todas as sugestões
- `GET /api/v1/suggestions/{campaign_id}` - Sugestões de uma campanha
- `POST /api/v1/suggestions/{id}/apply` - Aplicar sugestão

**Tipos de Sugestões:**
- 💰 **Budget:** "Aumente budget de 10% na Campanha X (ROI 3.5x)"
- ⏸️ **Pause:** "Pause Campanha Y (CPC R$ 2.50, meta R$ 0.80)"
- 🎨 **Creative:** "Troque criativos da Campanha Z (frequência 8.2, ideal <4)"
- 👥 **Audience:** "Expanda público da Campanha W (saturação 75%)"

---

### 2.5 Automação de Regras

| Feature | Descrição | Status |
|---------|-----------|--------|
| **Auto-Pause** | Pause campanha se CPC > threshold | ✅ |
| **Auto-Budget** | Ajuste budget baseado em ROI | ✅ |
| **Schedule Campaigns** | Ative/desative em horários específicos | ✅ |
| **Alerts** | Notificações via webhook/email | ✅ |

**Endpoints:**
- `POST /api/v1/automation/rules` - Criar regra
- `GET /api/v1/automation/rules` - Listar regras
- `PUT /api/v1/automation/rules/{id}` - Editar regra
- `DELETE /api/v1/automation/rules/{id}` - Deletar regra

**Exemplo de Regra:**
```json
{
  "name": "Pause High CPC Campaigns",
  "condition": {
    "metric": "cpc",
    "operator": ">",
    "value": 1.50,
    "period": "last_7_days"
  },
  "action": {
    "type": "pause_campaign",
    "notify": true
  }
}
```

---

### 2.6 Exportação de Métricas (NOVO)

| Feature | Descrição | Status |
|---------|-----------|--------|
| **Endpoint de Exportação** | `/api/v1/metrics/export` para sistemas externos | ✅ NOVO |
| **Autenticação via API Key** | Header `X-API-Key` | ✅ NOVO |
| **Rate Limiting** | 1000 requests/hora para analytics | ✅ NOVO |
| **Schemas Padronizados** | Pydantic models compartilhados | ✅ NOVO |

**Endpoint:**
```http
GET /api/v1/metrics/export?date_from=2025-10-17&date_until=2025-10-18
Headers:
  X-API-Key: {ANALYTICS_API_KEY}

Response:
{
  "campaigns": [
    {
      "campaign_id": "123",
      "campaign_name": "Campanha Teste",
      "date": "2025-10-18",
      "impressions": 10000,
      "clicks": 500,
      "spend": 250.00,
      "ctr": 5.0,
      "cpc": 0.50,
      "conversions": 50,
      "roas": 4.5
    }
  ],
  "total_campaigns": 1,
  "date_from": "2025-10-17",
  "date_until": "2025-10-18",
  "exported_at": "2025-10-18T10:30:00Z",
  "data_source": "facebook-ads-ai-agent",
  "version": "1.0.0"
}
```

---

### 2.7 Webhooks e Integrações

| Feature | Descrição | Status |
|---------|-----------|--------|
| **n8n Webhooks** | Notifica workflows externos | ✅ |
| **Slack Webhooks** | Alertas em canais Slack | ✅ |
| **Notion Integration** | Atualiza páginas Notion | ✅ |
| **Custom Webhooks** | POST para URL customizada | ✅ |

**Eventos Suportados:**
- `campaign.paused` - Campanha pausada
- `campaign.activated` - Campanha ativada
- `suggestion.created` - Nova sugestão gerada
- `threshold.exceeded` - Métrica ultrapassou limite
- `daily.report` - Relatório diário gerado

---

## 3. Arquitetura Técnica

### 3.1 Stack

```yaml
Backend: FastAPI (Python 3.12)
Database: PostgreSQL 15
Cache: Redis 7
Task Queue: Celery + Celery Beat
Authentication: JWT (PyJWT)
Rate Limiting: SlowAPI
Documentation: OpenAPI 3.1 (Swagger UI)
Monitoring: Prometheus + Grafana
Deployment: Docker + Docker Compose
```

### 3.2 Estrutura de Diretórios

```
api/
├── src/
│   ├── agents/          # FacebookAdsAgent (coleta Meta Ads)
│   ├── api/             # Routers FastAPI
│   │   ├── auth.py
│   │   ├── campaigns.py
│   │   ├── chat.py
│   │   ├── suggestions.py
│   │   ├── automation.py
│   │   └── metrics.py   # ⭐ NOVO: Exportação
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── tasks/           # Celery tasks
│   ├── utils/           # Helpers
│   └── integrations/    # n8n, Slack, Notion
├── tests/
├── alembic/             # Database migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── main.py
```

### 3.3 Database Schema

```sql
-- Campanhas Meta Ads
CREATE TABLE campaigns (
  id SERIAL PRIMARY KEY,
  campaign_id VARCHAR(255) UNIQUE,
  campaign_name VARCHAR(500),
  status VARCHAR(50),
  created_time TIMESTAMP,
  updated_time TIMESTAMP
);

-- Insights (métricas diárias)
CREATE TABLE insights (
  id SERIAL PRIMARY KEY,
  campaign_id INTEGER REFERENCES campaigns(id),
  date DATE,
  impressions INTEGER,
  clicks INTEGER,
  spend DECIMAL(10,2),
  reach INTEGER,
  frequency DECIMAL(5,2),
  ctr DECIMAL(5,2),
  cpc DECIMAL(10,2),
  conversions INTEGER,
  roas DECIMAL(10,2)
);

-- Sugestões
CREATE TABLE suggestions (
  id SERIAL PRIMARY KEY,
  campaign_id INTEGER REFERENCES campaigns(id),
  type VARCHAR(50),
  priority VARCHAR(20),
  message TEXT,
  data JSONB,
  status VARCHAR(50),
  created_at TIMESTAMP
);

-- Usuários
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  hashed_password VARCHAR(255),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP
);

-- Audit Logs
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  action VARCHAR(100),
  resource_type VARCHAR(50),
  resource_id INTEGER,
  details JSONB,
  created_at TIMESTAMP
);
```

---

## 4. Requisitos Não-Funcionais

### 4.1 Performance

| Requisito | Meta | Status |
|-----------|------|--------|
| Latência P95 < 200ms | < 200ms | ✅ 150ms |
| Throughput 100+ req/s | 100+ req/s | ✅ 120 req/s |
| Cache hit rate > 80% | > 80% | ✅ 85% |

### 4.2 Segurança

| Requisito | Status |
|-----------|--------|
| JWT com expiração 24h | ✅ |
| API Key rotation (trimestral) | 📅 Planejado |
| HTTPS only (produção) | ⚠️ Pendente |
| Rate limiting por IP | ✅ |
| Logs sem dados sensíveis | ✅ |

### 4.3 Escalabilidade

| Requisito | Status |
|-----------|--------|
| Suportar 10+ ad accounts | ✅ |
| Horizontal scaling | 📅 Planejado |
| PostgreSQL read replicas | 📅 Planejado |
| Redis cluster | 📅 Planejado |

### 4.4 Observabilidade

| Requisito | Status |
|-----------|--------|
| Logs estruturados (JSON) | ✅ |
| Métricas Prometheus | ✅ |
| Dashboards Grafana | ✅ |
| Health checks detalhados | ✅ |
| Alertas automáticos | 📅 Planejado |

---

## 5. Endpoints Completos

### Autenticação
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/users/me` - Perfil

### Campanhas
- `GET /api/v1/campaigns/` - Listar
- `GET /api/v1/campaigns/{id}` - Detalhe
- `GET /api/v1/campaigns/{id}/insights` - Insights
- `POST /api/v1/campaigns/sync` - Sincronizar

### Chat IA
- `POST /api/v1/chat` - Enviar mensagem
- `GET /api/v1/chat/history` - Histórico

### Sugestões
- `GET /api/v1/suggestions/` - Listar
- `GET /api/v1/suggestions/{campaign_id}` - Por campanha
- `POST /api/v1/suggestions/{id}/apply` - Aplicar

### Automação
- `POST /api/v1/automation/rules` - Criar regra
- `GET /api/v1/automation/rules` - Listar
- `PUT /api/v1/automation/rules/{id}` - Editar
- `DELETE /api/v1/automation/rules/{id}` - Deletar

### Exportação (NOVO)
- `GET /api/v1/metrics/export` - Exportar métricas
- `GET /api/v1/metrics/health` - Health check

### Webhooks
- `POST /api/v1/webhooks/n8n` - Receber de n8n
- `POST /api/v1/webhooks/slack` - Receber de Slack

### Saúde
- `GET /health` - Health check geral
- `GET /metrics` - Prometheus metrics

---

## 6. Métricas de Sucesso

| KPI | Meta | Atual |
|-----|------|-------|
| Latência P95 | < 200ms | ✅ 150ms |
| Taxa de erro | < 1% | ✅ 0.3% |
| Uptime | 99%+ | ✅ 99.5% |
| Cobertura testes | 80%+ | 📊 70% |
| Sugestões aceitas | 60%+ | 📊 Em medição |

---

## 7. Roadmap

### Q4 2025
- [x] Endpoint de exportação
- [x] Rate limiting diferenciado
- [x] Documentação completa
- [ ] HTTPS em produção
- [ ] Cobertura testes 80%+

### Q1 2026
- [ ] Horizontal scaling
- [ ] Read replicas PostgreSQL
- [ ] Alertas automáticos
- [ ] Dashboard Grafana customizado

### Q2 2026
- [ ] Multi-tenant (10+ clientes)
- [ ] API pública para terceiros
- [ ] Marketplace de automações

---

## 8. Referências

- [PRD-ANALYTICS.md](PRD-ANALYTICS.md) - PRD do Analytics
- [PRD-INTEGRATION.md](PRD-INTEGRATION.md) - Como se integram
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [API Docs](http://localhost:8000/docs) - Swagger UI

---

**Última atualização:** 18 de Outubro, 2025
**Versão:** 1.0.0
**Status (histórico):** Conteúdo reflete a implementação em 18/10/2025. Consulte `README.md` e `RELATORIO-CORRECOES-PENDENTES.md` para o panorama atual.
