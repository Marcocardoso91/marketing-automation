# Decisões Arquiteturais Consolidadas (ADR)

**Projeto:** Marketing Automation Platform
**Versão:** 1.0.0
**Data:** 18 de Outubro, 2025
**Status (histórico):** Decisões registradas até 18/10/2025. Reveja `RELATORIO-CORRECOES-PENDENTES.md` e ADRs específicos antes de adotar mudanças estruturais.

---

## Sumário

Este documento registra todas as **Decisões Arquiteturais (Architecture Decision Records - ADRs)** do Marketing Automation Platform, consolidando decisões dos projetos **Agent API**, **Analytics** e da **Integração** entre eles.

---

## ADRs do Agent API

### ADR-001: FastAPI como Framework Web

**Data:** 2025-10
**Status:** ✅ Aceito
**Contexto:** Necessidade de API REST rápida e moderna

**Alternativas:**
1. Django REST Framework - Mais pesado
2. Flask - Mais simples, menos features
3. **FastAPI** - Async, type hints, OpenAPI automático

**Decisão:** FastAPI

**Justificativa:**
- ✅ Performance superior (async/await)
- ✅ Documentação automática (Swagger UI)
- ✅ Validação com Pydantic
- ✅ Type hints nativos

---

### ADR-002: Celery para Tarefas Assíncronas

**Data:** 2025-10
**Status:** ✅ Aceito

**Decisão:** Celery + Celery Beat + Redis

**Justificativa:**
- ✅ Coleta de métricas não bloqueia API
- ✅ Agendamento (Celery Beat)
- ✅ Retry automático
- ✅ Escalável (múltiplos workers)

---

### ADR-003: PostgreSQL como Database Principal

**Data:** 2025-10
**Status:** ✅ Aceito

**Alternativas:**
1. MySQL
2. MongoDB
3. **PostgreSQL**

**Decisão:** PostgreSQL 15

**Justificativa:**
- ✅ JSONB para dados flexíveis
- ✅ Performance superior
- ✅ Transações ACID
- ✅ Extensões (pg_trgm para busca)

---

### ADR-004: JWT para Autenticação

**Data:** 2025-10
**Status:** ✅ Aceito

**Decisão:** JWT tokens (PyJWT)

**Justificativa:**
- ✅ Stateless (não precisa session store)
- ✅ Padrão indústria
- ✅ Fácil integração mobile/SPA
- ✅ Expiração automática

---

### ADR-005: Prometheus + Grafana para Monitoramento

**Data:** 2025-10
**Status:** ✅ Aceito

**Decisão:** Prometheus (métricas) + Grafana (dashboards)

**Justificativa:**
- ✅ Gratuito e open-source
- ✅ Padrão indústria
- ✅ Time-series database otimizado
- ✅ Alertas configuráveis

---

## ADRs do Analytics

### ADR-010: Supabase como Data Warehouse

**Data:** 2025-10-18
**Status:** ✅ Aceito

**Alternativas:**
1. BigQuery - Pago
2. PostgreSQL local - Manutenção
3. **Supabase** - PostgreSQL cloud gratuito

**Decisão:** Supabase (free tier)

**Justificativa:**
- ✅ Free tier 500MB
- ✅ PostgreSQL completo
- ✅ API REST automática
- ✅ Integração fácil com n8n
- ✅ Backup automático

---

### ADR-011: Arquitetura Modular de Workflows

**Data:** 2025-10-18
**Status:** ✅ Aceito

**Alternativas:**
1. Workflow monolítico
2. **Workflows modulares** (1 por fonte)

**Decisão:** 5 workflows n8n separados

**Justificativa:**
- ✅ Debugging isolado
- ✅ Falha em 1 não afeta outros
- ✅ Escalável (fácil adicionar fontes)
- ✅ Performance (execução paralela)

---

### ADR-012: Apache Superset para Visualização

**Data:** 2025-10-18
**Status:** ✅ Aceito

**Alternativas:**
1. Metabase
2. Grafana
3. **Apache Superset**
4. Tableau/Power BI (pago)

**Decisão:** Apache Superset (Docker)

**Justificativa:**
- ✅ 100% gratuito
- ✅ 40+ chart types
- ✅ SQL Lab para queries customizadas
- ✅ Múltiplas fontes de dados

---

### ADR-013: OpenAI para Insights Automatizados

**Data:** 2025-10-18
**Status:** ✅ Aceito

**Alternativas:**
1. Análise manual
2. Regras IF/THEN
3. **OpenAI GPT-4o-mini**
4. Claude
5. Gemini

**Decisão:** OpenAI GPT-4o-mini

**Justificativa:**
- ✅ Free tier 500 requests/mês
- ✅ Qualidade superior
- ✅ PT-BR nativo
- ✅ JSON mode

---

### ADR-001: n8n como Orquestrador

**Data:** 2025-10-11
**Status:** ✅ Aceito

**Alternativas:**
1. Zapier - Pago
2. Make - Pago
3. **n8n** - Open-source
4. Airflow - Mais complexo

**Decisão:** n8n (self-hosted)

**Justificativa:**
- ✅ Gratuito
- ✅ Self-hosted
- ✅ Interface visual
- ✅ Versionável (JSON)

---

### ADR-002: Notion como Database (Analytics)

**Data:** 2025-10-11
**Status:** ✅ Aceito (complementar ao Supabase)

**Decisão:** Notion para gestão visual

**Justificativa:**
- ✅ Interface superior
- ✅ Databases relacionais
- ✅ Colaboração nativa
- ✅ Usuária já familiarizada

**Nota:** Supabase é data warehouse técnico, Notion é interface de gestão

---

## ADRs da Integração

### ADR-014: Integração Híbrida via API REST

**Data:** 2025-10-18
**Status:** ✅ Aceito e Implementado

**Alternativas:**
1. **API REST** (escolhida)
2. Shared Database
3. Message Queue (RabbitMQ/Kafka)
4. Webhooks bidirecional is

**Decisão:** Agent API expõe endpoint REST para Analytics

**Justificativa:**
- ✅ Simplicidade (HTTP é universal)
- ✅ Desacoplamento (projetos independentes)
- ✅ Retry logic fácil de implementar
- ✅ Debugging simples (curl)
- ✅ Rate limiting granular

**Consequências Positivas:**
- Projetos mantêm independência
- Fonte única de dados Meta Ads
- Fácil adicionar novos consumidores

**Consequências Negativas:**
- Latência de rede (aceitável para batch diário)
- Dependência de Agent API estar UP

**Mitigação:**
- Health check antes de buscar
- Retry logic (3 tentativas)
- Script Python fallback

---

### ADR-015: Schemas Compartilhados com Pydantic

**Data:** 2025-10-18
**Status:** ✅ Aceito e Implementado

**Alternativas:**
1. Duplicar schemas em cada projeto
2. **Shared package** com Pydantic
3. OpenAPI code generation
4. Protocol Buffers (gRPC)

**Decisão:** Pacote Python `marketing_shared` com Pydantic models

**Justificativa:**
- ✅ Single source of truth
- ✅ Validação automática
- ✅ Type hints para IDE
- ✅ Fácil versionamento
- ✅ Instalável via pip

**Consequências Positivas:**
- Consistência de dados garantida
- Reduz erros de parsing
- Documentação inline

**Consequências Negativas:**
- Requer instalação em ambos projetos
- Mudanças devem ser coordenadas

**Mitigação:**
- Versionamento semântico
- Testes de integração
- CI/CD valida compatibilidade

---

### ADR-016: Estrutura Monorepo com Subprojetos

**Data:** 2025-10-18
**Status:** ✅ Aceito e Implementado

**Alternativas:**
1. Repositórios separados
2. **Monorepo** com subprojetos
3. Git submodules

**Decisão:** Monorepo `marketing-automation/` com api/, analytics/, shared/

**Justificativa:**
- ✅ Código compartilhado fácil
- ✅ Commits atômicos (mudança em shared + api)
- ✅ CI/CD unificado
- ✅ Documentação centralizada

**Estrutura:**
```
marketing-automation/
├── api/              # Agent API
├── analytics/        # Analytics
├── shared/           # Código compartilhado
├── docs/             # Documentação integrada
├── tests/            # Testes de integração
└── scripts/          # Scripts de automação
```

---

### ADR-017: Rate Limiting Diferenciado

**Data:** 2025-10-18
**Status:** ✅ Aceito e Implementado

**Alternativas:**
1. Rate limit único para todos
2. **Rate limit diferenciado** por tipo de cliente

**Decisão:** 1000 req/h para analytics, 100 req/min para usuários JWT

**Justificativa:**
- ✅ Analytics só precisa 1 request/dia
- ✅ Proteção contra abuse
- ✅ Limite generoso para evitar erros

**Implementação:**
```python
@limiter.limit("1000/hour")  # Para analytics
@limiter.limit("100/minute")  # Para usuários JWT
```

---

### ADR-018: Docker Compose para Deploy Local

**Data:** 2025-10-18
**Status:** ✅ Aceito e Implementado

**Alternativas:**
1. Kubernetes
2. **Docker Compose**
3. Deploy nativo

**Decisão:** Docker Compose com docker-compose.integrated.yml

**Justificativa:**
- ✅ Simplicidade
- ✅ Ambiente replicável
- ✅ Rollback fácil (snapshots)
- ✅ Suficiente para escala atual

**Serviços:**
- agent-api
- postgres
- redis
- celery-worker
- celery-beat
- superset
- prometheus (opcional)
- grafana (opcional)

---

## ADRs de Segurança

### ADR-005: Segurança de Tokens via .env

**Data:** 2025-10-11
**Status:** ✅ Aceito
**Prioridade:** 🔴 Crítico

**Alternativas:**
1. Hardcoded
2. **.env** (escolhida)
3. Docker Secrets
4. HashiCorp Vault

**Decisão:** Arquivo .env (gitignored) + env.example

**Justificativa:**
- ✅ Padrão indústria
- ✅ Simples de usar
- ✅ Compatível com Docker Compose, n8n, Python

**Regras:**
- ❌ NUNCA commitar .env
- ✅ .env.example versionado (sem valores)
- ✅ Rotação trimestral de API keys

---

## Sumário de Decisões Ativas

| ADR | Título | Projeto | Status |
|-----|--------|---------|--------|
| ADR-001 | FastAPI | Agent API | ✅ |
| ADR-002 | Celery | Agent API | ✅ |
| ADR-003 | PostgreSQL | Agent API | ✅ |
| ADR-004 | JWT | Agent API | ✅ |
| ADR-005 | Prometheus + Grafana | Agent API | ✅ |
| ADR-001 | n8n Orquestrador | Analytics | ✅ |
| ADR-002 | Notion Database | Analytics | ✅ |
| ADR-010 | Supabase Data Warehouse | Analytics | ✅ |
| ADR-011 | Workflows Modulares | Analytics | ✅ |
| ADR-012 | Apache Superset | Analytics | ✅ |
| ADR-013 | OpenAI Insights | Analytics | ✅ |
| **ADR-014** | **API REST Integration** | **Integração** | ✅ |
| **ADR-015** | **Shared Pydantic Schemas** | **Integração** | ✅ |
| **ADR-016** | **Monorepo Structure** | **Integração** | ✅ |
| **ADR-017** | **Rate Limiting Diferenciado** | **Integração** | ✅ |
| **ADR-018** | **Docker Compose** | **Integração** | ✅ |
| ADR-005 | Segurança .env | Todos | ✅ |

**Total:** 16 decisões documentadas

---

## Decisões Futuras (Em Avaliação)

### DEC-FUTURE-001: GraphQL API

**Contexto:** Alternativa ao REST para queries complexas
**Status:** 📅 Q1 2026
**Complexidade:** Alta
**Benefício:** Redução de overfetching

---

### DEC-FUTURE-002: gRPC para Alta Performance

**Contexto:** Alternativa ao REST HTTP/JSON
**Status:** 📅 Q1 2026
**Complexidade:** Alta
**Benefício:** 10x mais rápido que REST

---

### DEC-FUTURE-003: Kubernetes para Deploy

**Contexto:** Substituir Docker Compose
**Status:** 📅 Q2 2026 (quando escalar >10 clientes)
**Complexidade:** Muito Alta
**Benefício:** Auto-scaling, self-healing

---

### DEC-FUTURE-004: Machine Learning para Previsão

**Contexto:** Prever performance de campanhas
**Status:** 📅 Q2 2026
**Complexidade:** Muito Alta
**Benefício:** Redução 40% criativos baixa performance

---

## Referências

- [PRD-AGENT-API.md](PRD-AGENT-API.md)
- [PRD-ANALYTICS.md](PRD-ANALYTICS.md)
- [PRD-INTEGRATION.md](PRD-INTEGRATION.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Última atualização:** 18 de Outubro, 2025
**Responsável:** Marco @ Macspark
**Versão:** 1.0.0
