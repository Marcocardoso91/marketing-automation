# Índice da Documentação - Marketing Automation Platform

## 📚 Navegação Rápida

### 🏗️ Arquitetura

- [ARCHITECTURE.md](./architecture/ARCHITECTURE.md) - Visão geral da arquitetura do sistema
- [ADR-CONSOLIDATED.md](./architecture/ADR-CONSOLIDATED.md) - Architecture Decision Records (decisões técnicas)
- [DEPENDENCIES.md](./architecture/DEPENDENCIES.md) - Mapa de dependências e pacotes

### 📦 Produto

- [PRD-AGENT-API.md](./product/PRD-AGENT-API.md) - Product Requirements Document - Agent API
- [PRD-ANALYTICS.md](./product/PRD-ANALYTICS.md) - Product Requirements Document - Analytics
- [PRD-INTEGRATION.md](./product/PRD-INTEGRATION.md) - Product Requirements Document - Integração
- [BACKLOG.md](./product/BACKLOG.md) - Backlog de features e melhorias

### 💻 Desenvolvimento

- [QUICK-START.md](./development/QUICK-START.md) - Guia de início rápido (15 minutos)
- [CONTRIBUTING.md](./development/CONTRIBUTING.md) - Como contribuir com o projeto
- [SETUP-DATABASE.md](./development/SETUP-DATABASE.md) - Configuração do banco de dados

### 🚀 Operações

- [INTEGRATION-GUIDE.md](./operations/INTEGRATION-GUIDE.md) - Guia de integração completo
- [PROJECT-CONTEXT.md](./operations/PROJECT-CONTEXT.md) - Contexto e histórico do projeto

### 📊 Analytics

- [Analytics README](../analytics/README.md) - Visão geral do analytics (pipelines, workflows N8N, BI)
- [Analytics Docs](../analytics/docs/README.md) - Documentação histórica do Projeto Sabrina (v3.0)
- Guias de Setup:
  - [Setup Supabase](../analytics/docs/setup-supabase.md) - Data warehouse gratuito
  - [Setup N8N](../analytics/docs/setup-n8n-meta-ads.md) - Workflows automatizados
  - [Setup Apache Superset](../analytics/docs/setup-apache-superset.md) - Business Intelligence
  - [Setup Slack](../analytics/docs/setup-slack.md) - Notificações

### 📋 Decisões

- [ACOES-RECOMENDADAS.md](./decisions/ACOES-RECOMENDADAS.md) - Ações recomendadas para melhorias
- [DECISAO-MCP.md](./decisions/DECISAO-MCP.md) - Decisões sobre integração MCP
- [ROADMAP.md](./decisions/ROADMAP.md) - Roadmap de desenvolvimento

### 📚 Arquivo Histórico

- [Relatórios e Status](./archive/) - Relatórios históricos de implementação e validação

---

## 🚀 Começando

**Novo no projeto?** Comece por:

1. **[README.md](../README.md)** na raiz - Visão geral
2. **[👉-COMECE-AQUI.md](../👉-COMECE-AQUI.md)** - Guia de início
3. **[QUICK-START.md](./development/QUICK-START.md)** - Setup em 15 minutos
4. **[USER-GUIDE.md](./USER-GUIDE.md)** - Guia de uso diário
5. **[ARCHITECTURE.md](./architecture/ARCHITECTURE.md)** - Entender a arquitetura

**Desenvolvedor?**
1. **[CONTRIBUTING.md](./development/CONTRIBUTING.md)** - Diretrizes de contribuição
2. **[Backend README](../backend/README.md)** - Documentação específica do backend
3. **[Analytics README](../analytics/README.md)** - Documentação específica do analytics

**DevOps?**
1. **[Infrastructure README](../infrastructure/README.md)** - Configs Docker, monitoring, CI/CD
2. **[CI/CD Workflows](../.github/workflows/)** - GitHub Actions (testes, linting, Docker builds)
3. **[INTEGRATION-GUIDE.md](./operations/INTEGRATION-GUIDE.md)** - Guia de deploy

**Analytics/BI?**
1. **[Analytics README](../analytics/README.md)** - Pipelines de dados e workflows
2. **[Setup Guides](../analytics/docs/)** - Guias de setup das ferramentas

---

## 📊 Estrutura do Projeto

```
marketing-automation/
├── backend/          # FastAPI REST API
├── analytics/        # Data pipelines + BI
├── shared/           # Código compartilhado
├── frontend/         # Interface web (futuro)
├── infrastructure/   # Docker, monitoring, CI/CD
├── docs/            # Esta documentação
│   ├── architecture/
│   ├── product/
│   ├── development/
│   ├── operations/
│   ├── decisions/
│   └── archive/
└── tests/           # Testes de integração
```

---

## 🔗 Links Úteis

- **Repositório:** [GitHub](https://github.com/Marcocardoso91/marketing-automation)
- **Issues:** [GitHub Issues](https://github.com/Marcocardoso91/marketing-automation/issues)
- **API Docs:** http://localhost:8000/docs (quando rodando)
- **Superset:** http://localhost:8088 (quando rodando)

---

**Última atualização:** 20 de Outubro, 2025

