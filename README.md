# Marketing Automation Platform

> Monorepo que agrupa os componentes de automação (Agent API), analytics e o pacote Python compartilhado.

[![Issues](https://img.shields.io/github/issues/Marcocardoso91/marketing-automation)](https://github.com/Marcocardoso91/marketing-automation/issues)
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

**📋 [Ver Roadmap Completo](./docs/decisions/ROADMAP.md)** | **📊 [Análise Técnica](./docs/archive/ANALISE-TECNICA-COMPLETA.md)** | **🐛 [Issues](https://github.com/Marcocardoso91/marketing-automation/issues)**

---

## 🚀 Início Rápido

**Quer começar AGORA?** → **[START-HERE.md](START-HERE.md)** - Guia completo em 3 passos (30-45 minutos)

**Documentação completa** → [docs/INDEX.md](docs/INDEX.md)

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

## 🚀 Quick Start

### 1. Pré-requisitos

- ✅ Docker & Docker Compose
- ✅ Python 3.12+
- ✅ Git
- ✅ Conta Facebook Business Manager

### 2. Instalação Rápida (15 min)

```bash
# Clone o repositório
cd C:\Users\marco\Macspark\marketing-automation

# Setup automatizado
.\scripts\setup.ps1

# Editar credenciais
notepad .env  # Configurar Facebook + Supabase

# Subir serviços
docker-compose -f docker-compose.integrated.yml up -d
```

### 3. Verificar Sistema

```bash
# Health check
.\scripts\health-check.ps1

# Testar coleta de métricas
cd analytics\scripts
python metrics-to-supabase.py
```

### 4. Acessar Interfaces

- **Agent API:** http://localhost:8000/docs (Swagger UI)
- **Superset:** http://localhost:8088 (Dashboards BI)
- **Prometheus:** http://localhost:9090 (Métricas)

### 5. 🤖 MCP (Model Context Protocol)

Para agentes de IA acessarem a documentação:

```bash
# Configurar MCP
cd mcp-server
npm install && npm run build

# Usar com Claude Desktop ou outros clientes MCP
# Ver: docs/MCP-DOCUMENTATION-GUIDE.md
```

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

## 📚 Documentação Essencial

### 🎯 Para Iniciantes
- **[QUICK-START.md](docs/getting-started/QUICK-START.md)** – Setup em 15 minutos
- **[USER-GUIDE.md](docs/USER-GUIDE.md)** – Guia de uso diário
- **[INSTALLATION.md](docs/getting-started/INSTALLATION.md)** – Instalação detalhada

### 🏗️ Arquitetura & Design
- **[ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)** – Visão macro da solução
- **[INTEGRATION-GUIDE.md](docs/operations/INTEGRATION-GUIDE.md)** – Guia de integração
- **[MCP-DOCUMENTATION-GUIDE.md](docs/MCP-DOCUMENTATION-GUIDE.md)** – MCP para agentes IA

### 🔧 Desenvolvimento
- **[CONTRIBUTING.md](docs/development/CONTRIBUTING.md)** – Como contribuir
- **[API-REFERENCE.md](docs/api/agent-api/API-REFERENCE.md)** – Referência da API
- **[TROUBLESHOOTING.md](docs/reference/troubleshooting/TROUBLESHOOTING.md)** – Problemas comuns

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
