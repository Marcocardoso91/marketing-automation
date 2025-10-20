# Arquitetura - Marketing Automation Platform

> **Status (histórico):** Arquitetura vigente em 18/10/2025. Revise `README.md` e `RELATORIO-CORRECOES-PENDENTES.md` para o desenho atual.

## Visão Geral

Sistema distribuído com arquitetura de microservices integrados via API REST.

## Componentes Principais

### 1. Agent API (facebook-ads-ai-agent)

**Responsabilidades:**
- Fonte única de dados Meta Ads
- Automação inteligente de campanhas
- Chat com IA para consultas
- API REST com 22 endpoints

**Stack:**
- FastAPI (Python 3.12)
- PostgreSQL (dados estruturados)
- Redis (cache + Celery)
- Celery (tarefas assíncronas)
- JWT authentication
- SlowAPI (rate limiting)

**Endpoints Principais:**
- `POST /api/v1/auth/login` - Autenticação
- `GET /api/v1/campaigns/` - Listar campanhas
- `GET /api/v1/metrics/export` - **Exportar para analytics (NOVO)**
- `POST /api/v1/automation/*` - Sugestões de automação
- `POST /api/v1/chat` - Chat com IA

### 2. Analytics (Agente Facebook)

**Responsabilidades:**
- Coleta multi-canal (Meta via API, GA4, Google Ads, YouTube direto)
- Data warehouse (Supabase PostgreSQL)
- Visualização (Apache Superset)
- Insights IA (OpenAI)
- Notificações (Slack)

**Stack:**
- Python scripts
- n8n (orquestração de workflows)
- Supabase (PostgreSQL cloud)
- Apache Superset (BI)
- OpenAI API

**Workflows n8n:**
1. Meta Ads → busca do Agent API (9:45h) **MODIFICADO**
2. Google Analytics → coleta direta (9:00h)
3. Google Ads → coleta direta (9:15h)
4. YouTube → coleta direta (9:30h)
5. Consolidação + IA + Slack (10:00h)

### 3. Shared Package

**Responsabilidades:**
- Schemas Pydantic para validação
- Cliente HTTP com retry logic
- Utilitários compartilhados

**Instalação:**
```bash
pip install -e ./shared
```

**Uso:**
```python
from marketing_shared.schemas.facebook_metrics import CampaignMetricSchema
from marketing_shared.utils.api_client import AgentAPIClient
```

## Fluxo de Dados Detalhado

### Coleta de Meta Ads (INTEGRADO)

```
1. Facebook Marketing API
   ↓
2. Agent API (coleta via SDK)
   - Valida credenciais
   - Faz chamadas à API
   - Armazena em PostgreSQL local
   ↓
3. Endpoint /api/v1/metrics/export
   - Formata dados (CampaignMetricSchema)
   - Valida com Pydantic
   - Rate limit 1000/h
   ↓
4. Analytics (busca via HTTP)
   - AgentAPIClient com retry
   - Timeout 30s
   - 3 tentativas
   ↓
5. Supabase (data warehouse)
   - Consolida com outras fontes
   - Queries SQL avançadas
   ↓
6. Apache Superset (visualização)
   - Dashboards interativos
   - 40+ tipos de gráficos
```

### Coleta de Outras Fontes (DIRETO)

```
Google Analytics 4 ──┐
Google Ads ──────────┤
YouTube ─────────────┤→ Analytics scripts/n8n → Supabase
Instagram (manual) ──┘
```

## Decisões Arquiteturais

### ADR-014: Integração Híbrida via API REST

**Contexto:** Dois projetos com propósitos diferentes precisam compartilhar dados Meta Ads

**Decisão:** Agent API expõe endpoint REST, Analytics consome

**Alternativas Consideradas:**
- Fusão completa dos projetos (❌ complexidade alta)
- Compartilhamento de banco de dados (❌ acoplamento)
- Webhooks n8n (❌ menos robusto)

**Consequências:**
✅ Cada projeto mantém independência
✅ Coleta única de Meta Ads (economia de quota)
✅ Dados consistentes entre sistemas
✅ Fácil troubleshooting

### ADR-015: Schemas Compartilhados com Pydantic

**Contexto:** Garantir mesma estrutura de dados entre API e Analytics

**Decisão:** Pacote Python compartilhado com schemas Pydantic

**Consequências:**
✅ Validação automática
✅ Type safety
✅ Documentação inline
✅ Erros capturados em tempo de execução

### ADR-016: Estrutura Monorepo

**Contexto:** Gerenciar dois projetos + código compartilhado

**Decisão:** Monorepo com subprojetos (api/, analytics/, shared/)

**Consequências:**
✅ Código compartilhado fácil de manter
✅ CI/CD unificado
✅ Versionamento conjunto
⚠️ Requer disciplina em separação de concerns

## Segurança

### Autenticação

**Agent API:**
- JWT tokens (endpoints internos)
- API Key (endpoint de exportação) **NOVO**
- Rate limiting diferenciado

**Analytics:**
- API keys em variáveis de ambiente
- HTTPS obrigatório em produção

### Secrets Management

Todas as credenciais em `.env`:
```bash
FACEBOOK_ACCESS_TOKEN=xxx
ANALYTICS_API_KEY=xxx
SECRET_KEY=xxx
```

**Nunca** commitar `.env` no git!

## Escalabilidade

### Horizontal Scaling

**Agent API:**
- Múltiplas réplicas atrás de load balancer
- PostgreSQL com read replicas
- Redis cluster para cache

**Analytics:**
- n8n pode executar em cluster
- Supabase escala automaticamente

## Monitoramento

### Logs

```bash
docker logs marketing-agent-api
docker logs marketing-celery-worker
docker-compose -f docker-compose.integrated.yml logs -f
```

### Métricas (Prometheus)

```
- facebook_api_calls_total
- facebook_api_errors_total
- metrics_export_requests_total (NOVO)
- metrics_export_errors_total (NOVO)
```

### Health Checks

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/metrics/health
python scripts/validate-integration.py
```

---

**Versão:** 1.0.0  
**Data:** 2025-10-18

