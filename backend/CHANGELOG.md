# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-10-18

### 🎉 Lançamento Inicial

#### Adicionado

**Core Features:**
- Sistema completo de análise de campanhas do Facebook Ads
- Agente de IA para sugestões inteligentes de otimização
- Modo "suggestion-only" (não aplica mudanças automaticamente)
- Processamento de linguagem natural para chat

**Segurança:**
- Autenticação JWT completa
- Rate limiting em todos endpoints (SlowAPI)
- CORS restrito por ambiente
- SECRET_KEY seguro gerado
- Proteção de endpoints críticos
- 0 vulnerabilidades HIGH/MEDIUM (validado com Bandit e Safety)

**Analytics:**
- Sistema de scoring de campanhas (0-100)
- Análise de performance em tempo real
- Detecção de anomalias
- Tendências históricas
- Dashboard com métricas agregadas

**Automação:**
- Sugestões de pausa para campanhas underperforming
- Otimização automática de budgets
- Planos de realocação de verba
- Análise de ROI e performance

**Integrações:**
- Facebook Marketing API
- n8n (4 workflows ativos)
  - Coleta de métricas
  - Alertas multi-canal
  - WhatsApp via Evolution API
  - Email notifications
- Notion (salvamento de reports e sugestões)
- Slack (webhooks para alertas)
- WhatsApp (alertas críticos)
- Redis (cache e Celery broker)
- PostgreSQL (persistência)

**Monitoring & Observability:**
- Métricas Prometheus
- Dashboards Grafana
- Health check endpoint
- Structured logging
- Request tracking

**API Endpoints (21 total):**
- `/api/v1/auth/*` - Autenticação JWT
- `/api/v1/campaigns/*` - Gerenciamento de campanhas
- `/api/v1/analytics/*` - Analytics e reports
- `/api/v1/automation/*` - Automações e otimizações
- `/api/v1/chat` - Chat com IA
- `/api/v1/notion/*` - Integração Notion
- `/api/v1/n8n/*` - Gerenciamento n8n
- `/metrics` - Métricas Prometheus
- `/health` - Health check

**Celery Tasks:**
- Coleta de métricas do Facebook (30 min)
- Análise de performance (1 hora)
- Relatório diário (8h da manhã)
- Limpeza de dados antigos (domingo 2h)

**Testes:**
- Suite completa de testes unitários
- Testes de integração
- Coverage ~70%
- Validação de segurança automatizada
- Scripts de teste para cada integração

**Documentação:**
- README.md completo
- CONTRIBUTING.md
- CHANGELOG.md
- ROADMAP-MELHORIAS.md
- PLANO-IMPLEMENTADO-SUCESSO.md
- Docs de integrações (Notion, n8n)
- Docs de deployment
- Runbook operacional

**Scripts Utilitários:**
- `scripts/start_dev.py` - Inicia ambiente dev
- `scripts/health_check.py` - Verifica status do sistema
- `scripts/test_auth.py` - Testa autenticação JWT
- `scripts/test_facebook_connection.py` - Testa conexão Facebook
- `scripts/security_validation.py` - Validação de segurança
- `scripts/test_alertas_completos.py` - Testa todas integrações

**Infraestrutura:**
- Docker Compose (dev e prod)
- Traefik (proxy reverso + SSL)
- Alembic (migrations)
- Configuração Grafana
- Configuração Prometheus
- Deploy scripts

#### Segurança

- **Melhorias de Segurança:** Sistema passou de 4/10 para 8/10
- **Vulnerabilidades Resolvidas:**
  - Requests sem timeout (Bandit B113)
  - Atualizados: requests 2.31.0 → 2.32.5
  - Atualizados: python-jose 3.3.0 → 3.5.0
  - Atualizados: starlette 0.27.0 → 0.48.0
  - Atualizados: fastapi 0.104.1 → 0.119.0

#### Corrigido

- Import de classe inexistente em testes
- CORS permitindo qualquer origem
- Credenciais hardcoded no código
- Token manager sem timeout em requests
- Conflito de dependências (safety vs black)
- Metadata como coluna (palavra reservada SQLAlchemy)
- Schemas Pydantic com campos faltantes

#### Mudanças

**Breaking Changes:**
- Endpoints críticos agora requerem autenticação JWT
- Rate limiting ativo (pode limitar requests)
- CORS restrito (apenas origens específicas)

**Migrações:**
- Database schema inicial criada via Alembic
- Modelos: Campaign, Insight, User, ConversationMemory, Suggestion, AuditLog

#### Performance

- Rate limiting: 100 req/min (GET), 10 req/min (POST)
- Cache Redis configurado
- Async/await em todas operações IO
- Connection pooling (PostgreSQL)

---

## [Unreleased]

### Planejado para v1.1.0

- Dependency Injection
- LangChain para NLP avançado
- Circuit Breakers para APIs externas
- Cache Redis otimizado
- Cobertura de testes 85%+
- Testes E2E

Veja [ROADMAP-MELHORIAS.md](./ROADMAP-MELHORIAS.md) para detalhes.

---

## Formato de Versionamento

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades (compatível)
- **PATCH**: Correções de bugs (compatível)

Exemplo: 1.2.3
- 1 = Major version
- 2 = Minor version  
- 3 = Patch version

---

[1.0.0]: https://github.com/seu-org/facebook-ads-ai-agent/releases/tag/v1.0.0
[Unreleased]: https://github.com/seu-org/facebook-ads-ai-agent/compare/v1.0.0...HEAD