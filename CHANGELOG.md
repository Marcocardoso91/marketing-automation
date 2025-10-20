# Changelog - Marketing Automation Platform

## [1.1.0] - 2025-10-20

### Changed - Reorganização Completa de Estrutura

#### Limpeza Final da Raiz
- ✅ Movidos 9 documentos de processo para `docs/archive/process/`
- ✅ Raiz limpa: 3 docs essenciais + configs (era 12 docs)
- ✅ Criada pasta `docs/archive/process/` para docs de análise
- ✅ Estrutura 100% profissional e clean

### Changed - Reorganização de Estrutura

#### Estrutura de Pastas
- ✅ Renomeado `api/` → `backend/` (convenção monorepo)
- ✅ Criado `infrastructure/` para configs centralizadas
- ✅ Criado `frontend/` como placeholder
- ✅ Reorganizado `docs/` por categorias:
  - `docs/architecture/` - Arquitetura e ADRs
  - `docs/product/` - PRDs e backlog
  - `docs/development/` - Guias de desenvolvimento
  - `docs/operations/` - Deploy e operações
  - `docs/decisions/` - Decisões técnicas
  - `docs/archive/` - Relatórios históricos

#### Infraestrutura
- ✅ Movido `monitoring/prometheus.yml` → `infrastructure/monitoring/`
- ✅ Copiado `backend/Dockerfile` → `infrastructure/docker/backend.Dockerfile`
- ✅ Atualizado `docker-compose.integrated.yml` com novos paths

#### Documentação
- ✅ Atualizado README.md com nova estrutura
- ✅ Criado `docs/INDEX.md` navegável
- ✅ Criado `frontend/README.md` com planejamento
- ✅ Movidos relatórios históricos para `docs/archive/`
- ✅ Atualizado `👉-COMECE-AQUI.md` com novos paths
- ✅ Movido `RESUMO-FINAL.txt` → `docs/archive/RESUMO-INTEGRACAO-v1.0.0.txt`
- ✅ Movido `test_facebook.py` → `scripts/test-facebook.py`

#### Benefícios
- Estrutura mais clara e profissional
- Melhor navegação da documentação
- Preparado para expansão (frontend)
- Alinhado com best practices monorepo Python/FastAPI

## [1.0.0] - 2025-10-18

### Added - Integração Completa

#### Código Compartilhado
- ✅ Pacote Python `marketing-shared` instalável
- ✅ Schemas Pydantic compartilhados (`CampaignMetricSchema`, `ExportedMetricsResponse`)
- ✅ Cliente HTTP com retry logic (`AgentAPIClient`)
- ✅ Tratamento robusto de erros (`AgentAPIError`)

#### Agent API (api/)
- ✅ Novo endpoint `GET /api/v1/metrics/export`
- ✅ Autenticação via X-API-Key header
- ✅ Rate limiting 1000 requests/hora (SlowAPI)
- ✅ Dependency injection para FacebookAdsAgent
- ✅ Health check endpoint `/api/v1/metrics/health`
- ✅ Configuração `ANALYTICS_API_KEY` em Settings

#### Analytics (analytics/)
- ✅ Função `get_meta_ads_metrics()` modificada
- ✅ Integração com `AgentAPIClient`
- ✅ Workflow n8n `meta-ads-supabase.json` atualizado
- ✅ Node HTTP Request substituindo Facebook Graph API
- ✅ Variáveis de ambiente atualizadas (AGENT_API_URL, ANALYTICS_API_KEY)

#### Infraestrutura
- ✅ Docker Compose integrado com 7 serviços
- ✅ Health checks em todos os containers
- ✅ Inicialização automática do Superset
- ✅ Configuração Prometheus para monitoramento
- ✅ Volumes persistentes (postgres_data, superset_data)

#### Documentação
- ✅ README.md principal
- ✅ INTEGRATION-GUIDE.md (guia de integração)
- ✅ ARCHITECTURE.md (arquitetura detalhada)
- ✅ VALIDATION-CHECKLIST.md (checklist)
- ✅ MIGRATION.md (guia de migração)
- ✅ CHANGELOG.md (este arquivo)

#### Scripts
- ✅ `setup.ps1` - Setup automatizado (Windows)
- ✅ `health-check.ps1` - Verificação de saúde
- ✅ `validate-integration.py` - Validação de integração

#### Testes
- ✅ Testes de integração (`test_api_integration.py`)
- ✅ Testes de schemas Pydantic
- ✅ CI/CD com GitHub Actions

### Changed - Modificações

#### Agent API
- 📝 `main.py`: Importa novo router de metrics
- 📝 `requirements.txt`: Adiciona slowapi==0.1.9
- 📝 `src/utils/config.py`: Adiciona ANALYTICS_API_KEY
- 📝 Rate limiting configurado para novo endpoint

#### Analytics
- 📝 `scripts/metrics-to-supabase.py`: Usa AgentAPIClient
- 📝 `scripts/env.example.txt`: Variáveis de integração
- 📝 `scripts/requirements.txt`: Adiciona -e ../../shared
- 📝 `n8n-workflows/meta-ads-supabase.json`: HTTP Request node

### Removed - Deprecados

#### Analytics
- ❌ Acesso direto ao Facebook API (agora via Agent API)
- ❌ Variáveis `META_ACCESS_TOKEN` e `META_AD_ACCOUNT_ID` (movidas para comentário)
- ❌ Dependência direta da Facebook SDK no analytics

### Fixed - Correções

- 🐛 Conflito de nomes em Pydantic (date/datetime renomeados como Date/DateTime)
- 🐛 Imports corretos do pacote shared
- 🐛 Type hints compatíveis com Python 3.12

## Estrutura de Versionamento

- **Major** (1.x.x): Mudanças breaking na API ou estrutura
- **Minor** (x.1.x): Novas features sem breaking changes
- **Patch** (x.x.1): Bug fixes e melhorias

## Próximas Versões Planejadas

### [1.1.0] - Futuro
- Consolidação de PRDs
- ADRs unificados
- Backlogs consolidados
- Métricas de performance da integração

### [1.2.0] - Futuro
- Dashboards Grafana pré-configurados
- Alertas automáticos de integração
- Testes E2E completos

---

**Mantido por:** Macspark  
**Iniciado em:** 2025-10-18  
**Versão Atual:** 1.0.0

