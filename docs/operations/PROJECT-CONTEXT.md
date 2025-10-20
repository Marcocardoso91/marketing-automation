# Contexto do Projeto - Marketing Automation Platform

**Versão:** 1.0.0
**Data:** 18 de Outubro, 2025
**Status (histórico):** Panorama registrado em 18/10/2025. Confira `README.md` e `RELATORIO-CORRECOES-PENDENTES.md` para informações atualizadas.
**Owner:** Marco @ Macspark

---

## 1. Visão Geral

### O Que É

O **Marketing Automation Platform** é um sistema enterprise-grade que unifica dois projetos complementares:

1. **Agent API** - API REST inteligente para automação de Meta Ads
2. **Analytics** - Sistema multi-canal de análise e visualização

### Por Que Existe

**Problema Original:**
- Gestão fragmentada de marketing digital
- Coleta duplicada de dados Meta Ads
- Análise manual propensa a erros
- Decisões baseadas em dados desatualizados

**Solução:**
- Plataforma unificada que elimina duplicação
- Automação inteligente com IA
- Data warehouse centralizado
- Dashboards visuais e insights automáticos

---

## 2. Histórico

### Fase 1: Projetos Separados (Antes de Out 2025)

**facebook-ads-ai-agent:**
- Criado para automatizar Meta Ads
- 21 endpoints REST
- Chat IA para análise de campanhas
- Sugestões automáticas de otimização

**Agente Facebook (Projeto Sabrina):**
- Criado para campanha de crescimento Instagram
- Coleta multi-canal (Meta, GA4, Google Ads, YouTube)
- Dashboards no Notion e Apache Superset
- Insights IA diários

**Problema:** Ambos coletavam Meta Ads independentemente (duplicação)

### Fase 2: Integração (18 Out 2025)

- ✅ Criado pacote Python compartilhado (`marketing_shared`)
- ✅ Agent API expõe endpoint `/api/v1/metrics/export`
- ✅ Analytics busca Meta Ads do Agent API (não mais do Facebook direto)
- ✅ Código compartilhado (schemas Pydantic, cliente HTTP)
- ✅ Documentação consolidada (3 PRDs, ADRs, arquitetura)

---

## 3. Stakeholders

| Stakeholder | Papel | Interesse |
|-------------|-------|-----------|
| **Marco** | Owner/Dev | Manter sistema funcionando, escalar |
| **Sabrina** | Usuária Principal (Analytics) | Crescer Instagram, otimizar campanhas |
| **Clientes Futuros** | Potenciais usuários | Multi-tenant, API pública |
| **Comunidade OS** | Desenvolvedores | Open-source futuro (Q3 2026) |

---

## 4. Tecnologias Core

### Agent API
- FastAPI (Python 3.12)
- PostgreSQL 15
- Redis 7
- Celery + Celery Beat
- Prometheus + Grafana

### Analytics
- n8n (workflows)
- Supabase (PostgreSQL cloud)
- Apache Superset (BI)
- OpenAI GPT-4o-mini
- Slack Webhooks

### Integração
- marketing_shared (pacote Python)
- Pydantic (schemas)
- HTTP REST API
- Docker Compose

---

## 5. Ambiente de Desenvolvimento

### Estrutura

```
marketing-automation/
├── api/          # Agent API
├── analytics/    # Analytics
├── shared/       # Código compartilhado
├── docs/         # Documentação
├── tests/        # Testes
└── scripts/      # Automação
```

### Setup Local

```bash
# 1. Instalar shared package
cd shared && pip install -e .

# 2. Configurar .env
cp env.template .env
nano .env  # Adicionar credenciais

# 3. Subir stack
docker-compose -f docker-compose.integrated.yml up -d

# 4. Validar
python scripts/validate-integration.py
```

---

## 6. Ambiente de Produção

### Infraestrutura

- **VPS:** Linux Ubuntu 22.04
- **Docker:** Engine 24.x
- **Domínio:** macspark.dev
- **Proxy:** Traefik (planejado) ou Nginx

### URLs

- Agent API: `https://api.macspark.dev` (planejado)
- Superset: `https://bi.macspark.dev` (planejado)
- n8n: `https://fluxos.macspark.dev` (existente)

---

## 7. Métricas de Sucesso

### Negócio
- ROI campanhas: 2,5-3,5x
- Custo por seguidor: R$ 1,00-1,30
- Tempo análise: < 20 min/dia
- Novos seguidores: 900-1.300/mês

### Técnicas
- Uptime: 99%+
- Latência P95: < 200ms
- Taxa erro: < 1%
- Cobertura testes: 80%+

---

## 8. Riscos e Dependências

### Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Facebook API changes | Média | Alto | Monitorar changelog, testes |
| Downtime Agent API | Baixa | Alto | Fallback script Python |
| Estouro Supabase | Baixa | Médio | Arquivamento mensal |
| Custo OpenAI | Média | Baixo | Cache insights |

### Dependências Críticas

- Facebook API (Meta)
- Supabase (data warehouse)
- OpenAI API (insights)
- VPS (hospedagem)

---

## 9. Roadmap Resumido

- **Q4 2025:** Produção com HTTPS, testes 80%
- **Q1 2026:** Horizontal scaling, novas integrações (TikTok, LinkedIn)
- **Q2 2026:** Multi-tenant, API pública
- **Q3 2026:** Open-source

---

## 10. Onboarding para Novos Desenvolvedores

### Passo 1: Leia a Documentação

1. [README.md](../README.md) - Visão geral
2. [QUICK-START.md](../QUICK-START.md) - Setup em 15 min
3. [PRD-AGENT-API.md](PRD-AGENT-API.md)
4. [PRD-ANALYTICS.md](PRD-ANALYTICS.md)
5. [PRD-INTEGRATION.md](PRD-INTEGRATION.md)
6. [ARCHITECTURE.md](ARCHITECTURE.md)

### Passo 2: Setup Local

```bash
./scripts/setup.ps1  # Windows
# ou
./scripts/setup.sh   # Linux/Mac
```

### Passo 3: Execute Testes

```bash
pytest tests/integration/ -v
```

### Passo 4: Faça Uma Mudança Simples

- Adicione um teste em `tests/integration/`
- Modifique um schema em `shared/marketing_shared/schemas/`
- Crie um novo endpoint em `backend/src/api/`

### Passo 5: Abra um Pull Request

- Siga convenções de commit (Conventional Commits)
- Garanta que testes passam
- Atualize documentação se necessário

---

## 11. FAQ

### Como funciona a integração entre Agent API e Analytics?

Analytics busca dados Meta Ads do Agent API via HTTP GET (`/api/v1/metrics/export`) ao invés de coletar direto do Facebook. Isso elimina duplicação e garante consistência.

### Por que dois projetos separados?

Cada projeto tem responsabilidades distintas:
- **Agent API:** Automação inteligente Meta Ads
- **Analytics:** Análise multi-canal

A integração via API permite independência enquanto compartilha dados.

### Posso usar apenas um dos projetos?

Sim! São independentes:
- Use apenas **Agent API** se só precisa automação Meta Ads
- Use apenas **Analytics** se já tem outra fonte de dados Meta Ads

### Como adicionar nova fonte de dados no Analytics?

1. Crie novo workflow n8n (`n8n-workflows/nova-fonte.json`)
2. Configure coleta da API externa
3. Transforme dados para schema Supabase
4. Insira no Supabase
5. Atualize dashboard Superset

---

## 12. Recursos Úteis

- **Swagger UI (Agent API):** http://localhost:8000/docs
- **Superset:** http://localhost:8088
- **n8n:** https://fluxos.macspark.dev
- **Supabase Dashboard:** https://app.supabase.com
- **Prometheus:** http://localhost:9090 (se ativo)
- **Grafana:** http://localhost:3000 (se ativo)

---

## 13. Contato e Suporte

- **Owner:** Marco @ Macspark
- **Issues:** Abra issue no repositório GitHub
- **Docs:** [INDEX.md](../INDEX.md)

---

**Última atualização:** 18 de Outubro, 2025
**Versão:** 1.0.0
