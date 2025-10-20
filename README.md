# Marketing Automation Platform

> Monorepo que agrupa os componentes de automação (Agent API), analytics e o pacote Python compartilhado.

[![Issues](https://img.shields.io/github/issues/Marcocardoso28/marketing-automation)](https://github.com/Marcocardoso28/marketing-automation/issues)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📊 Status do Projeto

| Métrica | Status |
|---------|--------|
| **Análise Técnica** | ✅ Completa (2025-10-19) |
| **Issues Identificadas** | 26 (5 P0, 6 P1, 10 P2, 5 P3) |
| **Roadmap** | 📅 3 Sprints planejados |
| **Cobertura de Testes** | ⚠️ Parcial (muitos skips) |
| **Segurança** | 🔴 Atenção necessária |

**📋 [Ver Roadmap Completo](./ROADMAP.md)** | **📊 [Análise Técnica](./ANALISE-TECNICA-COMPLETA.md)** | **🐛 [Issues](https://github.com/Marcocardoso28/marketing-automation/issues)**

---

## Visão Geral

| Diretório  | Descrição | Status atual |
|------------|-----------|--------------|
| `backend/`     | FastAPI + Celery para orquestrar Facebook Ads, chat IA e exportação de métricas. | ✅ Produção (rotinas core) |
| `analytics/` | Scripts e workflows n8n para coleta multi‑fonte. Dashboards BI com Apache Superset. | ✅ Operacional |
| `shared/`  | Pacote Python com schemas Pydantic e utilitários reutilizáveis. | ✅ |
| `docs/`    | Documentação organizada por categoria (architecture, product, development, operations). | ✅ |
| `infrastructure/` | Configurações Docker, monitoring (Prometheus) e CI/CD. | ✅ |
| `frontend/` | Placeholder para interface web futura (atualmente usa Swagger + Superset). | 📋 Planejado |

> ℹ️ Servidores MCP não residem neste repositório. Use o projeto `mcp_orchestrator` (Node/TypeScript) ou os servidores comunitários mencionados no guia de MCP para expor ferramentas a agentes externos.

### Estrutura Simplificada

```
marketing-automation/
├── backend/          -> FastAPI (Agent API) + Celery
├── analytics/        -> Data pipelines + BI (Superset)
├── shared/           -> Pacote Python (schemas/utilitários)
├── frontend/         -> Interface web (futuro)
├── infrastructure/   -> Docker, monitoring, CI/CD
├── docs/             -> Documentação organizada
└── tests/            -> Testes de integração
```

## Quick Start

### 1. Pré-requisitos

- Docker & Docker Compose
- Python 3.12+
- Git

### 2. Instalação básica

```bash
# Clone o repositório
cd C:\Users\marco\Macspark\marketing-automation

# Preparar variáveis para Agent API
cp env.template .env
# Edite .env com credenciais reais antes do deploy

# Setup automatizado (Windows)
.\scripts\setup.ps1
```

### 3. Subir a stack integrada (opcional)

```bash
docker-compose -f docker-compose.integrated.yml up -d
docker-compose -f docker-compose.integrated.yml logs -f
```

### 4. Endereços úteis

- Agent API: http://localhost:8000/docs  
- Superset / Grafana / Prometheus: conforme perfis ativados no `docker-compose.integrated.yml`

## Destaques por Componente

### Agent API (`api/`)
- Exporta métricas via `GET /api/v1/metrics/export` (header `X-API-Key`).
- Endpoints autenticados com JWT e protegidos por rate limiting/middlewares de segurança.
- Tarefas Celery para coleta/análise; métricas Prometheus expostas.

### Analytics (`analytics/`)
- Scripts Python (`scripts/metrics-to-supabase.py`) e workflows n8n prontos como template.
- Parte da documentação descreve metas/planos (mantida para histórico). Consulte `IMPLEMENTACAO-v3.0-COMPLETA.md` e guias de setup antes de executar.

### Shared (`shared/`)
- `marketing_shared` fornece schemas Pydantic e utilitários compartilhados.
- Cliente HTTP com retry logic e wrapper unificado do Facebook Graph (`marketing_shared.utils.facebook_client`).

## Documentação Essencial

- `docs/ARCHITECTURE.md` – visão macro da solução.
- `docs/INTEGRATION-GUIDE.md` – guia de integração passo a passo.
- PRDs consolidados em `analytics/docs/prd/agente-facebook/` (os arquivos em `api/docs/prd/facebook-ads-agent/` são apenas redirecionamentos).
- `api/docs/MCP-INTEGRATION.md` – como conectar agentes via MCP (n8n/Notion) usando servidores externos.
- `api/docs/CREDENCIAIS-TEMPORARIAS.md` – política de credenciais e boas práticas de segurança.

## Desenvolvimento

### Ambiente local
```bash
# Dependências do Agent API
cd api
pip install --break-system-packages -r requirements.txt

# Scripts de analytics (opcional)
cd ../analytics/scripts
pip install -r requirements.txt
```

### Testes
```bash
cd api
PYTHONPATH=.:../shared pytest
```
Os testes de integração já mockam autenticação e pulam fluxos que exigem `.env` ou n8n real.

## Suporte e Referências

- Documentação detalhada em `docs/` e nos subdiretórios de cada projeto.
- Pendências e próximos passos consolidados em `RELATORIO-CORRECOES-PENDENTES.md`.
- Integrações MCP: executar servidores externos (ex.: `n8n-mcp-server`) conforme `api/docs/MCP-INTEGRATION.md` e o projeto `mcp_orchestrator`.

---

> Este repositório mantém a compatibilidade com integrações REST tradicionais. Utilize MCP apenas quando precisar que um agente externo componha fluxos dinamicamente.
