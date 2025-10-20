<!-- be822876-c11f-45bd-9ed0-937175305986 abb67760-7459-4304-a4d1-97632a986058 -->
# Plano: Finalizar Projeto para Produção

## Objetivo

Tornar o projeto Marketing Automation Platform **100% funcional e utilizável**, resolvendo pendências críticas e validando fluxo completo.

## Situação Atual

✅ **O que está PRONTO:**

- Estrutura reorganizada (backend/, docs/, infrastructure/)
- Docker Compose configurado
- Shared package funcional
- Supabase conectado e operacional
- N8N nodes disponíveis
- Scripts de automação funcionais
- Credenciais Facebook obtidas

⚠️ **O que FALTA:**

- Facebook API permissões (erro 403)
- Docs principais com refs antigas (103 ocorrências)
- Validação end-to-end completa
- Configurações opcionais (Slack, Notion)

**Score atual: 95%** → Meta: **100%**

## Etapas de Implementação

### ETAPA 1: Resolver Facebook API (CRÍTICO)

**Problema:** Erro 403 - "Ad account owner has NOT grant ads_management permission"

**Solução Manual (Usuário deve fazer):**

1. Acessar https://business.facebook.com/settings
2. Ir em "Contas" → "Apps" → "Marketing API" (ID: 833349949092216)
3. Configurar permissões para "Conta 01" (act_659480752041234):

   - ads_management
   - ads_read
   - business_management

**Validação:**

```bash
python scripts/test-facebook.py
# Deve retornar: Status 200 ✅
```

**Tempo:** 5-10 minutos (manual)

**Bloqueador:** SIM - Sem isso, coleta de métricas não funciona

---

### ETAPA 2: Atualizar Docs Principais

**Problema:** 103 referências a "api/" em docs consultados regularmente

**Arquivos a atualizar:**

- `docs/architecture/ARCHITECTURE.md` (8 refs)
- `docs/architecture/ADR-CONSOLIDATED.md` (2 refs)
- `docs/product/PRD-AGENT-API.md` (42 refs)
- `docs/product/PRD-INTEGRATION.md` (15 refs)
- `docs/operations/INTEGRATION-GUIDE.md` (4 refs)
- `docs/development/SETUP-DATABASE.md` (2 refs)
- `docs/decisions/DECISAO-MCP.md` (10 refs)
- Outros (20 refs distribuídas)

**Ação:** Find & replace "api/" → "backend/" onde apropriado

**Exceções (NÃO mudar):**

- `/api/v1/*` (são paths HTTP de endpoints)
- `src/api/` (estrutura interna do backend)
- docs/archive/* (documentos históricos)

**Tempo:** 20 minutos

**Bloqueador:** NÃO - Projeto funciona sem isso

---

### ETAPA 3: Validar Stack Docker

**Objetivo:** Garantir que todos containers sobem corretamente

**Ações:**

1. Rebuild containers com contexto atualizado:
   ```bash
   docker-compose -f docker-compose.integrated.yml build --no-cache
   ```

2. Subir stack completa:
   ```bash
   docker-compose -f docker-compose.integrated.yml up -d
   ```

3. Verificar health de todos serviços:
   ```bash
   .\scripts\health-check.ps1
   ```

4. Validar logs:
   ```bash
   docker-compose -f docker-compose.integrated.yml logs --tail=50
   ```


**Problemas conhecidos:**

- Permissões Docker em alguns containers (já identificado)
- Porta 6379 conflito (já resolvido → 6380)

**Tempo:** 30 minutos

**Bloqueador:** PARCIAL - API pode rodar local sem Docker

---

### ETAPA 4: Testar Fluxo End-to-End

**Objetivo:** Validar fluxo completo backend → analytics → supabase

**Cenário de teste:**

1. Backend coleta métricas do Facebook
2. Analytics consome via `/api/v1/metrics/export`
3. Dados salvos no Supabase
4. Dashboards Superset mostram dados

**Steps:**

```bash
# 1. Verificar backend
curl http://localhost:8000/health

# 2. Testar endpoint métricas (com API key)
curl -H "X-API-Key: ${ANALYTICS_API_KEY}" \
  "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-18&date_until=2025-10-18"

# 3. Executar script analytics
cd analytics/scripts
python metrics-to-supabase.py

# 4. Verificar Supabase
# Acessar Supabase console e ver tabela daily_metrics
```

**Tempo:** 15 minutos

**Bloqueador:** SIM - Depende de ETAPA 1 (Facebook)

---

### ETAPA 5: Configurar Integrações Opcionais

**Objetivo:** Configurar Slack, Notion (se desejado)

**Slack (Notificações):**

1. Criar webhook: https://api.slack.com/messaging/webhooks
2. Adicionar no `.env`: `SLACK_WEBHOOK_URL=...`
3. Testar: `python analytics/scripts/test-slack-webhook.py`

**Notion (Relatórios):**

1. Criar integration: https://www.notion.so/my-integrations
2. Compartilhar database com integration
3. Adicionar no `.env`: `NOTION_API_TOKEN=...` e `NOTION_DATABASE_ID=...`

**OpenAI (Chat IA):**

1. Obter API key: https://platform.openai.com/api-keys
2. Adicionar no `.env`: `OPENAI_API_KEY=sk-...`

**Tempo:** 30-60 minutos (opcional)

**Bloqueador:** NÃO - Features extras

---

### ETAPA 6: Criar Guia de Uso Final

**Objetivo:** Documentar como usar o sistema no dia-a-dia

**Criar:** `docs/USER-GUIDE.md`

**Conteúdo:**

```markdown
# Guia de Uso - Marketing Automation Platform

## Uso Diário

### 1. Verificar Saúde do Sistema
.\scripts\health-check.ps1

### 2. Coletar Métricas Manualmente
cd analytics/scripts
python metrics-to-supabase.py

### 3. Ver Dashboards
- Superset: http://localhost:8088
- Prometheus: http://localhost:9090

### 4. Consultar API
http://localhost:8000/docs

## Troubleshooting

### Facebook 403
- Verificar permissões no Business Manager
- Renovar token (expira em 60 dias)

### Docker não sobe
- Verificar portas em uso
- Limpar cache: docker system prune
```

**Tempo:** 30 minutos

**Bloqueador:** NÃO

---

### ETAPA 7: Validação Final Completa

**Objetivo:** Garantir que tudo funciona perfeitamente

**Checklist:**

**Backend:**

- [ ] API responde em http://localhost:8000/health
- [ ] Swagger UI acessível em /docs
- [ ] Endpoint `/api/v1/metrics/export` retorna dados
- [ ] Autenticação funciona (X-API-Key)
- [ ] Rate limiting ativo

**Analytics:**

- [ ] Script `metrics-to-supabase.py` executa sem erros
- [ ] Dados aparecem no Supabase
- [ ] Workflows N8N importam corretamente

**Infraestrutura:**

- [ ] Todos containers healthy
- [ ] PostgreSQL aceita conexões
- [ ] Redis funcional
- [ ] Superset inicializa

**Documentação:**

- [ ] Todos links funcionando
- [ ] READMEs em todas pastas
- [ ] Guias atualizados

**Tempo:** 30 minutos

**Bloqueador:** NÃO

---

## Riscos e Mitigações

**Risco 1:** Facebook não aprovar permissões

**Mitigação:** Usar System User Token alternativo

**Risco 2:** Docker não funcionar em Windows

**Mitigação:** Executar API localmente com Python

**Risco 3:** Credenciais Supabase inválidas

**Mitigação:** Já validado com MCP - está funcionando

## Ordem de Execução

**Crítico (Fazer AGORA):**

1. ETAPA 1 - Facebook permissões (Manual, 10 min)
2. ETAPA 3 - Validar Docker (30 min)
3. ETAPA 4 - Teste end-to-end (15 min)

**Importante (Fazer hoje):**

4. ETAPA 2 - Atualizar docs (20 min)
5. ETAPA 7 - Validação final (30 min)

**Opcional (Quando necessário):**

6. ETAPA 5 - Integrações extras (60 min)
7. ETAPA 6 - Guia de uso (30 min)

## Tempo Total

**Mínimo (Apenas crítico):** 55 minutos

**Recomendado (Crítico + Importante):** 2 horas

**Completo (Tudo):** 4 horas

## Critérios de Sucesso

**Projeto está pronto quando:**

- ✅ Facebook API retorna 200
- ✅ Backend coleta métricas do Facebook
- ✅ Analytics salva dados no Supabase
- ✅ Dashboards mostram dados
- ✅ Docker stack funcional
- ✅ Documentação 100% atualizada

**Score mínimo:** 98%

**Score ideal:** 100%

### To-dos

- [ ] Configurar permissões Facebook no Business Manager (CRÍTICO - manual)
- [ ] Rebuild e validar Docker stack completa
- [ ] Testar fluxo completo: backend → analytics → supabase
- [ ] Atualizar docs principais: api/ → backend/ (103 refs)
- [ ] Executar validação final completa (checklist)
- [ ] Configurar Slack, Notion, OpenAI (opcional)
- [ ] Criar docs/USER-GUIDE.md com guia de uso diário