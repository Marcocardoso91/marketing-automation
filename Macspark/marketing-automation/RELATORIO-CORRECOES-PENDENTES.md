# Relatório de Correções Pendentes

Inventário completo dos problemas identificados no projeto **marketing-automation**. O foco está em corrigir falhas críticas de rota, segurança e consistência antes de novas entregas.

## 1. Problemas Críticos
- ✅ `api/src/api/metrics.py`: rota refatorada para consumir campanhas reais e emitir `CampaignMetricSchema`.
- ✅ `api/src/schemas/campaign_schemas.py`: campo `synced_at` tornou-se opcional e populado no agente.
- ✅ `api/src/api/auth.py`: autenticação usa banco/hashed password e troca de senha revoga token.
- ✅ `api/src/utils/config.py`: validação impede secrets padrão em produção e permite configurar origens confiáveis.
- ✅ `api/docker-compose.yml`: credenciais exigem variáveis fortes e `.env` atualizado com placeholders obrigatórios.
- ✅ `api/src/api/notion.py`: comparação usa `campaign_id` e gera sugestões corretas.
- ✅ `api/src/utils/context_memory.py`: histórico persistido com `AsyncSession` e validação por usuário autenticado.

- ✅ `api/src/api/n8n_admin.py`: entradas via body + respostas 501 quando MCP indisponível.
- ✅ `api/src/agentes/*` e `shared/marketing_shared/utils/api_client.py`: cliente unificado (wrapper compartilhado).
- ✅ `analytics/scripts/metrics-to-supabase.py`: processamento ajustado ao novo payload do endpoint.
- ✅ `tests/integration/test_api_integration.py` (raiz) agora encapsula os testes de `api/tests` e evita divergência de lógica.
- ✅ Documentação redundante (`api/docs/prd/facebook-ads-agent/*` agora aponta para `analytics/docs/prd/agente-facebook/*` como fonte única).

- ✅ `api/src/api/campaigns.py`: uso de `Depends(get_facebook_agent)` para reuso e tratamento de falhas de inicialização.
- ⚠️ `api/src/integrations/notion_client.py` e `api/src/integrations/n8n_manager.py`: integração MCP segue não implementada (apenas placeholders e logs).
- ✅ `api/src/tasks/*`: tratativas extras para falhas de init/listagem e métricas de erro adicionadas.
- ✅ `api/tests/test_suite_completa.py`: testes que exigem `.env` ou n8n real são marcados como `skip`.
- ✅ API de chat `/api/v1/chat`: agora exige autenticação + rate limit.

- ✅ Prometheus: `docker-compose.yml` agora referencia o arquivo único em `monitoring/prometheus.yml`.
- ✅ `env.template`: placeholders atualizados com instruções explícitas e valores obrigatórios.
- ⚠️ Relatórios/documentos históricos mantidos (com notas), ainda requerem revisão completa.
- ⚠️ Documentação analytics continua referenciando workflows MCP não implementados.
- ✅ `.gitignore` ampliado para cobrir caches e artefatos adicionais.

## 5. Arquivos/Recursos Duplicados
- PRDs e backlog: `api/docs/prd/facebook-ads-agent/*` vs `analytics/docs/prd/agente-facebook/*`.
- `README.md` em múltiplos diretórios (`/`, `api/`, `analytics/`, `shared/`, `analytics/scripts/`, `analytics/n8n-workflows/`). Padronizar estrutura e linkar seções em vez de copiar.
- Roteiro de Prometheus: `api/config/prometheus.yml` e `monitoring/prometheus.yml`.
- `requirements.txt`: `api/requirements.txt` vs `analytics/scripts/requirements.txt`. Considere reunir em `requirements/` com extras (`api`, `analytics`).
- Testes de integração: arquivos homônimos em `api/tests/integration/` e `tests/integration/`.

## 6. Plano de Ação Sugerido
1. **Segurança & Autenticação**
   - Implementar fluxo de login baseado em banco com hashing (`passlib`) e tokens revogáveis.
   - Forçar substituição de secrets (`SECRET_KEY`, `ANALYTICS_API_KEY`) e credenciais Docker por variáveis seguras.
2. **Restaurar rota `/metrics/export`**
   - Ajustar schema `CampaignResponse`/`CampaignMetricSchema`.
   - Atualizar testes e o script `metrics-to-supabase.py`.
3. **Persistência de contexto e integrações**
   - Implementar `ContextManager` com `AsyncSession` e corrigir lógica Notion (`campaign_id`).
   - Completar (ou desabilitar explicitamente) integração MCP para Notion/n8n.
4. **Higiene de código e documentação**
   - Remover/centralizar duplicidades de docs, requisitos e testes.
   - Atualizar relatórios e checklists para refletirem pendências reais.
5. **Observabilidade & Resiliência**
   - Revisar tasks Celery, adicionar métricas de falha e circuit breaker para tokens.
   - Estender suite de testes com mocks para Facebook/n8n/Notion, garantindo execução em CI.

## 7. Próximos Passos Imediatos
1. Completar implementação MCP (n8n/Notion) utilizando servidores externos (`mcp_orchestrator` ou pacotes comunitários) e integrar agente.
2. Revisar documentação legada (PRDs, relatórios históricos) para refletir o status atual ou sinalizar claramente conteúdo histórico.
3. Consolidar READMEs/requirements restantes (subprojetos) onde fizer sentido, mantendo referência única por tema.

Após concluir os itens críticos, executar `pytest api/tests` com mocks e scripts de integração para validar `/metrics`, `/auth` e `/chat`.***
