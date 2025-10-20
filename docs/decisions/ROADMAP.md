# 🗺️ Roadmap - Marketing Automation Platform

**Última atualização**: 2025-10-19
**Status**: Análise técnica completa realizada
**Total de issues**: 26 (25 técnicas + 1 operacional)

---

## 📊 Visão Geral

| Prioridade | Quantidade | Esforço Estimado | Sprint |
|------------|------------|------------------|--------|
| 🔴 P0 (Crítico) | 5 | 7-9h | Sprint 1 |
| 🟠 P1 (Alto) | 6 | 18-26h | Sprint 1 |
| 🟡 P2 (Médio) | 10 | 33-43h | Sprint 2-3 |
| 🟢 P3 (Baixo) | 5 | 13-17h | Backlog |

**Esforço Total**: 71-95 horas (~2-3 sprints de 2 semanas)

---

## 🎯 Sprint 1 (2 semanas) - CRÍTICOS & SEGURANÇA

**Objetivo**: Resolver problemas bloqueadores e críticos de segurança

**Data prevista**: IMEDIATO - Primeiras 2 semanas

### Prioridade MÁXIMA (primeiras 48h)

- [ ] **[P0] Remover .env do Git + rotacionar credenciais** (3h)
  - Risco de segurança CRÍTICO
  - Rotacionar: SECRET_KEY, N8N_API_KEY, NOTION_API_TOKEN

- [ ] **[P0] Migration hashed_password** (30min)
  - Blocker para produção

### Semana 1

- [ ] **[P0] Migrar TokenBlacklist para Redis** (2h)
  - Tokens revogados voltam ativos após restart

- [ ] **[P0] Cache FacebookAdsAgent** (1h)
  - -300ms latência por request

- [ ] **[P0/P1] Decisão sobre MCP** (2h cleanup OU 16-24h implementação)
  - Escolher: Implementar ou remover código fake

- [ ] **[P1] Circuit Breaker para APIs externas** (4h)
  - Prevenir cascade failures

- [ ] **[P1] Refatorar error handling** (6h)
  - 43 exceções genéricas → hierarquia de exceções

### Semana 2

- [ ] **[P1] Métricas de erro no Celery** (3h)
  - Tasks podem falhar silenciosamente

- [ ] **[P1] Remover código duplicado de API client** (1h)
  - Camada de indireção desnecessária

- [ ] **[P1] Testes com mocks 100% funcionais** (8h)
  - Eliminar testes skipped

- [ ] **[P2] Configurar n8n inicial** (4h)
  - Sistema vazio detectado: 0 workflows, 0 credenciais

**Total Sprint 1**: 25-49h (depende da decisão sobre MCP)

---

## 🚀 Sprint 2 (2 semanas) - QUALIDADE & PERFORMANCE

**Objetivo**: Melhorias de código, docs e performance

**Data prevista**: Semanas 3-4

### Código & Arquitetura

- [ ] **[P1] Índices de DB** (1h)
- [ ] **[P2] Validação async (não sync)** (2h)
- [ ] **[P2] Type hints completos** (12h)
  - Atualmente ~60%, meta: 95%+

### Documentação

- [ ] **[P2] Consolidar docs duplicadas** (6h)
  - READMEs, PRDs em múltiplos lugares

- [ ] **[P2] Gerenciamento de deps centralizado** (4h)
  - Monorepo com requirements/ estruturado

### Performance & API

- [ ] **[P2] Implementar paginação** (3h)
- [ ] **[P2] CORS com validação runtime** (2h)
- [ ] **[P2] Refatorar CampaignOptimizer** (4h)
  - Remover lógica hardcoded

**Total Sprint 2**: 34h

---

## 📈 Sprint 3 (2 semanas) - DEVOPS & MELHORIA CONTÍNUA

**Objetivo**: DevOps, observabilidade e processos

**Data prevista**: Semanas 5-6

### DevOps

- [ ] **[P3] Pre-commit hooks** (1h)
  - Black, flake8, mypy

- [ ] **[P3] Atualizar dependências** (4h)
  - fastapi, openai, langchain

- [ ] **[P3] Prometheus alerts** (3h)
  - Alertmanager configurado

### Observabilidade

- [ ] **[P3] Correlation IDs em logs** (3h)
- [ ] **[P3] Testes de carga com Locust** (4h)

### Documentação

- [ ] **[P3] ADRs (Architecture Decision Records)** (4h)
- [ ] **[P3] Trackear TODOs** (2h)
  - 7 TODOs no código → issues

**Total Sprint 3**: 21h

---

## 📦 Backlog / Futuro

### Features Planejadas

- **MCP Real** (se decidir implementar em Sprint 1)
  - Integração completa Notion
  - Integração completa n8n
  - Esforço: 16-24h

### Melhorias Técnicas

- **Migração para Poetry/Pipenv** (6h)
  - Melhor gerenciamento de deps

- **Kubernetes Deployment** (16h)
  - Escalabilidade automática

- **Rate Limiting mais sofisticado** (4h)
  - Por endpoint, por usuário

- **Audit Log completo** (8h)
  - Rastreamento de todas ações

---

## 📐 Métricas de Sucesso

### Sprint 1
- ✅ 0 credenciais expostas no git
- ✅ 100% dos testes rodando (sem skips)
- ✅ Latência média < 200ms (vs 500ms atual)
- ✅ 0 tokens revogados válidos após restart

### Sprint 2
- ✅ Cobertura de testes > 80%
- ✅ Type hints > 95%
- ✅ Docs consolidadas (1 fonte de verdade)
- ✅ Todas queries < 100ms

### Sprint 3
- ✅ Pre-commit hooks ativos
- ✅ Alertas configurados (Prometheus)
- ✅ ADRs documentando decisões
- ✅ Deps atualizadas (sem vulnerabilidades)

---

## 🔗 Links Importantes

### GitHub
- **Issues**: [Ver todas as issues](https://github.com/Marcocardoso28/marketing-automation/issues)
- **Project Board**: [Kanban Board](https://github.com/Marcocardoso28/marketing-automation/projects)
- **Milestones**:
  - [Sprint 1 - Críticos](https://github.com/Marcocardoso28/marketing-automation/milestone/1)
  - [Sprint 2 - Qualidade](https://github.com/Marcocardoso28/marketing-automation/milestone/2)
  - [Sprint 3 - DevOps](https://github.com/Marcocardoso28/marketing-automation/milestone/3)

### Documentação
- [Análise Técnica Completa](./ANALISE-TECNICA-COMPLETA.md)
- [README Principal](./README.md)
- [Arquitetura](./docs/ARCHITECTURE.md)

---

## 🎬 Como Usar Este Roadmap

### 1. Criar Issues no GitHub

```bash
# Configure suas credenciais
export GITHUB_TOKEN=your_github_personal_access_token
export GITHUB_REPO=owner/repo  # ex: Marcocardoso28/marketing-automation

# Execute o script
cd scripts
python create-github-issues.py

# Ou dry-run primeiro
python create-github-issues.py --dry-run
```

### 2. Acompanhar Progresso

1. Acesse o **Project Board** no GitHub
2. Issues organizadas em colunas:
   - 📋 Backlog
   - 🔥 Sprint 1 (P0/P1)
   - ⏭️ Sprint 2 (P2)
   - 📅 Sprint 3 (P3)
   - ✅ Done

### 3. Trabalhar em Uma Issue

```bash
# 1. Criar branch
git checkout -b fix/issue-123-token-blacklist

# 2. Implementar
# ... fazer código ...

# 3. Testar
pytest

# 4. Commit
git commit -m "fix: migrate TokenBlacklist to Redis (#123)"

# 5. Push e PR
git push origin fix/issue-123-token-blacklist
gh pr create --fill
```

---

## 📞 Suporte

- **Dúvidas técnicas**: Abrir issue no GitHub
- **Discussões**: GitHub Discussions
- **Urgências**: Marcar como `priority-urgent`

---

**Roadmap mantido por**: Equipe de Desenvolvimento
**Próxima revisão**: Após Sprint 1 (2 semanas)
