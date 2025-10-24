# Índice da Documentação - Marketing Automation Platform

**Versão:** 2.0.0  
**Última atualização:** 23 de Outubro, 2025  
**Status:** ✅ Reestruturado e Otimizado com MCP

---

## 🚀 Navegação Rápida

### 🎯 Getting Started
- [QUICK-START.md](./getting-started/QUICK-START.md) - Início rápido (15 minutos)
- [INSTALLATION.md](./getting-started/INSTALLATION.md) - Instalação detalhada (30-45 min)
- [FIRST-STEPS.md](./getting-started/FIRST-STEPS.md) - Primeiros passos após instalação

### 🏗️ Arquitetura
- [OVERVIEW.md](./architecture/ARCHITECTURE.md) - Visão geral da arquitetura
- [DECISIONS.md](./architecture/ADR-CONSOLIDATED.md) - Architecture Decision Records
- [DEPENDENCIES.md](./architecture/DEPENDENCIES.md) - Mapa de dependências

### 📖 Guias por Tipo
- **User Guides:** [USER-GUIDE.md](./USER-GUIDE.md) - Uso diário do sistema
- **Developer:** [CONTRIBUTING.md](./development/CONTRIBUTING.md) - Como contribuir
- **Operations:** [INTEGRATION-GUIDE.md](./operations/INTEGRATION-GUIDE.md) - Deploy e operações

### 🔌 API & Integrações
- **Agent API:** [API-REFERENCE.md](./api/agent-api/API-REFERENCE.md) - Endpoints completos
- **N8N Integration:** [N8N-GUIDE.md](./api/integrations/N8N-GUIDE.md) - Workflows automatizados
- **Notion Integration:** [NOTION-GUIDE.md](./api/integrations/NOTION-GUIDE.md) - Relatórios

### 📋 Referência
- **Troubleshooting:** [TROUBLESHOOTING.md](./reference/troubleshooting/TROUBLESHOOTING.md) - Problemas comuns
- **Configuration:** [ENV-VARS.md](./reference/configuration/ENV-VARS.md) - Variáveis de ambiente
- **Glossary:** [GLOSSARY.md](./reference/GLOSSARY.md) - Termos técnicos

### 📊 Analytics & BI
- [Analytics README](../analytics/README.md) - Visão geral do analytics
- [Setup Supabase](../analytics/docs/setup-supabase.md) - Data warehouse
- [Setup N8N](../analytics/docs/setup-n8n-meta-ads.md) - Workflows automatizados
- [Setup Superset](../analytics/docs/setup-apache-superset.md) - Business Intelligence

### 🚀 Produção & Deploy
- [📋 Checklist de Produção](operations/PRODUCTION-READINESS-CHECKLIST.md) - O que falta para produção
- [🚀 Guia de Deploy](operations/PRODUCTION-DEPLOYMENT-GUIDE.md) - Deploy completo em produção
- [🔧 Setup Produção](../scripts/setup-production.sh) - Script automatizado de setup

### 🤖 MCP (Model Context Protocol)
- [MCP-DOCUMENTATION-GUIDE.md](./MCP-DOCUMENTATION-GUIDE.md) - Guia completo de uso MCP
- [mcp-config.json](../mcp-config.json) - Configuração MCP
- [mcp-server/](../mcp-server/) - Servidor MCP implementado

### 📚 Arquivo Histórico
- [Relatórios e Status](./archive/) - Relatórios históricos de implementação

---

## 🚀 Começando

### 👤 Novo no Projeto?
1. **[README.md](../README.md)** - Visão geral do projeto
2. **[QUICK-START.md](./getting-started/QUICK-START.md)** - Setup em 15 minutos
3. **[USER-GUIDE.md](./USER-GUIDE.md)** - Guia de uso diário
4. **[ARCHITECTURE.md](./architecture/ARCHITECTURE.md)** - Entender a arquitetura

### 👨‍💻 Desenvolvedor?
1. **[CONTRIBUTING.md](./development/CONTRIBUTING.md)** - Diretrizes de contribuição
2. **[Backend README](../backend/README.md)** - Documentação específica do backend
3. **[API-REFERENCE.md](./api/agent-api/API-REFERENCE.md)** - Referência completa da API

### 🔧 DevOps?
1. **[Infrastructure README](../infrastructure/README.md)** - Configs Docker, monitoring, CI/CD
2. **[INTEGRATION-GUIDE.md](./operations/INTEGRATION-GUIDE.md)** - Guia de deploy
3. **[CI/CD Workflows](../.github/workflows/)** - GitHub Actions

### 📊 Analytics/BI?
1. **[Analytics README](../analytics/README.md)** - Pipelines de dados e workflows
2. **[Setup Guides](../analytics/docs/)** - Guias de setup das ferramentas
3. **[Superset Setup](../analytics/docs/setup-apache-superset.md)** - Business Intelligence

### 🤖 Usando MCP?
1. **[MCP-DOCUMENTATION-GUIDE.md](./MCP-DOCUMENTATION-GUIDE.md)** - Guia completo MCP
2. **[mcp-config.json](../mcp-config.json)** - Configuração MCP
3. **[mcp-server/](../mcp-server/)** - Servidor MCP implementado

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

