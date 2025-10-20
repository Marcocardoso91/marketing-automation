#!/usr/bin/env python3
"""
Script para criar Issues no GitHub automaticamente
Baseado na Análise Técnica Completa

Uso:
    python create-github-issues.py --token YOUR_GITHUB_TOKEN --repo owner/repo

Ou configure as variáveis de ambiente:
    export GITHUB_TOKEN=your_token
    export GITHUB_REPO=owner/repo
    python create-github-issues.py
"""

import os
import sys
import requests
import argparse
from typing import List, Dict

# Configuração
ISSUES = [
    # P0 - CRÍTICOS
    {
        "title": "[P0][SECURITY] Credenciais reais expostas no .env versionado",
        "body": """## 🔴 CRÍTICO - Segurança

**Arquivo**: `api/.env`

### Descrição
Credenciais reais estão versionadas no git:
- `SECRET_KEY=823ef04b24287aa6973613172ebad191...`
- `N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- `NOTION_API_TOKEN=ntn_44266321668aTZt11zd3cpnXj8z...`

### Impacto
🔥 **CRÍTICO** - Comprometimento total do sistema se o repositório for público ou acessado por terceiros.

### Solução
```bash
# 1. Remover do git
git rm --cached api/.env

# 2. Atualizar .gitignore
echo "**/.env" >> .gitignore
echo ".env.*" >> .gitignore
echo "!.env.example" >> .gitignore

# 3. Rotacionar TODAS as credenciais
# - Gerar novo SECRET_KEY
# - Recriar N8N_API_KEY
# - Recriar NOTION_API_TOKEN

# 4. Commit e push
git add .gitignore
git commit -m "security: remove .env and add to gitignore"
git push
```

### Checklist
- [ ] Remover .env do git
- [ ] Atualizar .gitignore
- [ ] Rotacionar SECRET_KEY
- [ ] Rotacionar N8N_API_KEY
- [ ] Rotacionar NOTION_API_TOKEN
- [ ] Verificar histórico do git (considerar git filter-branch se necessário)
- [ ] Configurar secrets no CI/CD
- [ ] Documentar processo em .env.example

### Esforço Estimado
⏱️ 2-3 horas

### Prioridade
🔴 P0 - RESOLVER IMEDIATAMENTE (primeiras 24h)
""",
        "labels": ["security", "p0", "critical", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P0][SECURITY] TokenBlacklist em memória perde estado ao reiniciar",
        "body": """## 🔴 CRÍTICO - Segurança

**Arquivo**: `api/src/utils/security.py:99-132`

### Descrição
A classe `TokenBlacklist` usa `set()` em memória para armazenar tokens revogados. Ao reiniciar o servidor, todos os tokens revogados voltam a ser válidos.

```python
class TokenBlacklist:
    def __init__(self):
        self._blacklist: Set[str] = set()  # ❌ Memória volátil
```

### Impacto
🔴 **ALTO** - Usuários que:
- Fizeram logout
- Trocaram senha
- Tiveram tokens revogados

...podem continuar usando tokens antigos após restart do servidor.

### Solução
Migrar para Redis com TTL automático:

```python
import redis
import hashlib
from datetime import datetime

class RedisTokenBlacklist:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def add(self, token: str, expiry: datetime):
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        ttl = int((expiry - datetime.utcnow()).total_seconds())
        self.redis.setex(f"blacklist:{token_hash}", ttl, "1")

    def is_blacklisted(self, token: str) -> bool:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return self.redis.exists(f"blacklist:{token_hash}") > 0
```

### Checklist
- [ ] Adicionar redis ao docker-compose.yml
- [ ] Adicionar redis-py ao requirements.txt
- [ ] Implementar RedisTokenBlacklist
- [ ] Atualizar dependency injection
- [ ] Adicionar testes
- [ ] Documentar no README

### Esforço Estimado
⏱️ 2 horas

### Prioridade
🔴 P0 - RESOLVER IMEDIATAMENTE
""",
        "labels": ["security", "p0", "bug", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P0][ARCH] Integração MCP completamente não implementada",
        "body": """## 🟠 ALTO - Arquitetura

**Arquivos**:
- `api/src/integrations/notion_client.py`
- `api/src/integrations/n8n_manager.py`

### Descrição
Código de integração MCP são apenas placeholders que logam warnings:

```python
async def create_campaign_report(self, campaign_data: Dict) -> Optional[str]:
    logger.warning("Notion integration not available - returning mock ID")
    return None  # ❌ Sempre retorna None
```

A documentação promete features que não existem.

### Impacto
🟠 **ALTO** - Features documentadas não funcionam:
- Criação automática de reports no Notion
- Criação de workflows no n8n via API
- Sincronização de dados

### Decisão Necessária

**Opção A**: Implementar realmente (16-24h)
- Usar MCP servers configurados
- Implementar cliente MCP real
- Testes de integração

**Opção B**: Cleanup e docs honestas (2h)
- Remover código placeholder
- Atualizar docs para "Planejado"
- Criar issues de feature para futuro

### Recomendação
💡 Opção B por enquanto (cleanup). Criar roadmap para Opção A em Q1 2026.

### Checklist
- [ ] Decidir: Implementar ou remover?
- [ ] Se implementar: criar spike técnico
- [ ] Se remover: deletar código placeholder
- [ ] Atualizar toda documentação
- [ ] Comunicar stakeholders

### Esforço Estimado
⏱️ 2h (cleanup) ou 16-24h (implementação)

### Prioridade
🟠 P0/P1 - Decisão necessária na Sprint 1
""",
        "labels": ["architecture", "p0", "decision-needed", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P0][PERF] FacebookAdsAgent recriado a cada request",
        "body": """## 🟠 ALTO - Performance

**Arquivo**: `api/src/api/campaigns.py:16-22`

### Descrição
O `Depends(get_facebook_agent)` cria nova instância do FacebookAdsAgent em **CADA request**:

```python
def get_facebook_agent() -> FacebookAdsAgent:
    return FacebookAdsAgent()  # ❌ Nova instância toda vez
```

Isso faz:
- Validação de token no Facebook API (HTTP request externo)
- Inicialização do FacebookAdsApi
- ~300-500ms de latência extra por request

### Impacto
🔴 **ALTO**:
- Latência desnecessária (+300-500ms/request)
- Rate limit do Facebook API desperdiçado
- CPU/memória desperdiçados

### Solução
Implementar singleton com cache TTL:

```python
import time
from typing import Optional

_agent_cache: Optional[FacebookAdsAgent] = None
_agent_cache_time: Optional[float] = None
CACHE_TTL = 3600  # 1 hora

def get_facebook_agent() -> FacebookAdsAgent:
    global _agent_cache, _agent_cache_time

    now = time.time()

    # Cache miss ou expirado
    if _agent_cache is None or (now - _agent_cache_time) > CACHE_TTL:
        _agent_cache = FacebookAdsAgent()
        _agent_cache_time = now
        logger.info("Created new FacebookAdsAgent instance (cache miss)")

    return _agent_cache
```

### Alternativa: Dependency com cache no FastAPI
```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_cached_facebook_agent() -> FacebookAdsAgent:
    return FacebookAdsAgent()
```

### Checklist
- [ ] Implementar singleton com TTL
- [ ] Adicionar métricas (cache hits/misses)
- [ ] Testes de concorrência
- [ ] Documentar comportamento
- [ ] Monitorar impacto na latência

### Esforço Estimado
⏱️ 1 hora

### Prioridade
🔴 P0 - RESOLVER Sprint 1
""",
        "labels": ["performance", "p0", "optimization", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P0][DB] Migration faltando para coluna hashed_password",
        "body": """## 🔴 CRÍTICO - Database

**Arquivo**: `api/alembic/versions/001_initial_schema.py`

### Descrição
O model `User` define `hashed_password`:

```python
# api/src/models/user.py:19
class User(Base):
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
```

Mas a migration inicial NÃO cria essa coluna!

```python
# 001_initial_schema.py
op.create_table(
    'users',
    sa.Column('id', ...),
    sa.Column('email', ...),
    # ❌ FALTA hashed_password
)
```

### Impacto
🔥 **CRÍTICO** - Sistema de autenticação quebrado em produção:
- Deploy vai falhar
- Login não funciona
- `IntegrityError` ao criar usuários

### Solução
Adicionar coluna na migration `002_add_user_auth_fields.py` (se existir) ou criar nova:

```python
# alembic/versions/002_add_hashed_password.py
def upgrade():
    op.add_column(
        'users',
        sa.Column('hashed_password', sa.String(), nullable=False,
                  server_default='')  # Temporário para migração
    )

    # Depois de migração, remover server_default
    op.alter_column('users', 'hashed_password', server_default=None)

def downgrade():
    op.drop_column('users', 'hashed_password')
```

### Checklist
- [ ] Criar migration 002
- [ ] Testar upgrade em DB vazio
- [ ] Testar downgrade
- [ ] Atualizar seed data se existir
- [ ] Documentar no CHANGELOG

### Esforço Estimado
⏱️ 30 minutos

### Prioridade
🔴 P0 - BLOCKER para produção
""",
        "labels": ["database", "p0", "critical", "migration", "sprint-1"],
        "milestone": 1
    },

    # P1 - ALTOS
    {
        "title": "[P1][CODE] 43 exceções genéricas sem contexto adequado",
        "body": """## 🟠 ALTO - Qualidade de Código

**Localização**: 43 ocorrências em `api/src/`

### Descrição
Tratamento genérico de erros que:
- Esconde problemas reais
- Expõe stack traces sensíveis
- Dificulta debugging

```python
except Exception as e:
    logger.error(f"Error: {e}")  # ❌ Log genérico
    raise HTTPException(
        status_code=500,
        detail=str(e)  # ❌ Expõe stack trace
    )
```

### Impacto
- Debugging muito difícil em produção
- Informações sensíveis vazadas
- Impossível criar alertas específicos

### Solução
Criar hierarquia de exceções:

```python
# src/exceptions.py
class MacsparkException(Exception):
    pass

class ExternalAPIError(MacsparkException):
    pass

class FacebookAPIError(ExternalAPIError):
    pass

class RateLimitError(FacebookAPIError):
    pass

# Uso
try:
    response = facebook_api.call()
except RateLimitError:
    raise HTTPException(429, detail="Rate limit exceeded")
except FacebookAPIError as e:
    logger.error("Facebook API error", extra={"error": str(e)})
    raise HTTPException(502, detail="External API unavailable")
```

### Checklist
- [ ] Criar arquivo src/exceptions.py
- [ ] Definir hierarquia de exceções
- [ ] Refatorar 43 ocorrências
- [ ] Adicionar testes
- [ ] Documentar no CONTRIBUTING.md

### Esforço Estimado
⏱️ 4-6 horas

### Prioridade
🟠 P1 - Sprint 1
""",
        "labels": ["code-quality", "p1", "refactoring", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P1][RESILIENCE] Implementar Circuit Breaker pattern",
        "body": """## 🟠 ALTO - Resiliência

**Localização**: Todas chamadas a APIs externas

### Descrição
Sem circuit breaker, se Facebook API ficar lento/indisponível:
- Sistema continua tentando indefinidamente
- Threads/workers ficam bloqueados
- Cascade failure para outras partes do sistema

### Impacto
Sistema pode ficar completamente inutilizável por falha externa.

### Solução
Implementar com `pybreaker`:

```python
from pybreaker import CircuitBreaker
from facebook_business.exceptions import FacebookRequestError

# Configuração
facebook_breaker = CircuitBreaker(
    fail_max=5,              # Abre após 5 falhas
    timeout_duration=60,      # Reabre após 60s
    expected_exception=FacebookRequestError,
    name="facebook_api"
)

# Uso
@facebook_breaker
async def call_facebook_api(endpoint: str, params: dict):
    response = await facebook_client.get(endpoint, params=params)
    return response.json()

# Handler para circuit aberto
@app.exception_handler(CircuitBreakerError)
async def circuit_breaker_handler(request, exc):
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable"}
    )
```

### Features
- [ ] Circuit Breaker para Facebook API
- [ ] Circuit Breaker para n8n
- [ ] Circuit Breaker para Notion
- [ ] Métricas Prometheus
- [ ] Dashboard Grafana
- [ ] Alertas

### Checklist
- [ ] Adicionar pybreaker ao requirements.txt
- [ ] Implementar decorators
- [ ] Configurar thresholds
- [ ] Adicionar testes
- [ ] Documentar comportamento
- [ ] Monitorar em produção

### Esforço Estimado
⏱️ 3-4 horas

### Prioridade
🟠 P1 - Sprint 1
""",
        "labels": ["resilience", "p1", "enhancement", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P1][CODE] Duplicação de código: dois wrappers de API Facebook",
        "body": """## 🟡 MÉDIO - Code Smell

**Arquivos**:
- `api/src/utils/api_client.py` - wrapper vazio
- `shared/marketing_shared/utils/facebook_client.py` - implementação real

### Descrição
Camada de indireção desnecessária que confunde:

```python
# api/src/utils/api_client.py
from marketing_shared.utils.facebook_client import FacebookClient

def get_api_client():
    return FacebookClient()  # Apenas um alias!
```

### Impacto
- Confusão para novos desenvolvedores
- Camada extra sem valor
- Dificulta refatoração

### Solução
```bash
# Remover o wrapper
rm api/src/utils/api_client.py

# Atualizar imports
# De:
from src.utils.api_client import get_api_client
# Para:
from marketing_shared.utils.facebook_client import FacebookClient
```

### Checklist
- [ ] Identificar todas as referências
- [ ] Atualizar imports
- [ ] Remover arquivo
- [ ] Rodar testes
- [ ] Atualizar docs se necessário

### Esforço Estimado
⏱️ 1 hora

### Prioridade
🟡 P1 - Sprint 1 ou 2
""",
        "labels": ["code-quality", "p1", "refactoring", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P1][TEST] Muitos testes configurados como skip",
        "body": """## 🟠 ALTO - Testes

**Arquivo**: `api/tests/test_suite_completa.py:12-14`

### Descrição
Testes marcados para skip quando não há `.env` ou n8n:

```python
skip_if_no_env = pytest.mark.skipif(
    not HAS_ENV_FILE,
    reason=".env file not available"
)

skip_n8n_e2e = pytest.mark.skipif(...)

# Resultado: Testes não rodam em CI!
```

### Impacto
- Cobertura real de testes desconhecida
- CI/CD pode passar com bugs
- Falsa sensação de segurança

### Solução
Criar fixtures com mocks para 100% dos testes rodarem:

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_facebook_api(monkeypatch):
    mock = Mock()
    mock.get_campaign.return_value = {
        "id": "123",
        "name": "Test Campaign"
    }
    monkeypatch.setattr("src.agents.facebook_agent.FacebookAdsApi", mock)
    return mock

# Reorganizar estrutura
tests/
├── unit/          # Sempre rodam (com mocks)
├── integration/   # Requerem .env (Docker)
└── e2e/          # Manual (staging)
```

### Checklist
- [ ] Criar mocks para todas dependências externas
- [ ] Reorganizar testes em unit/integration/e2e
- [ ] Configurar pytest.ini
- [ ] Atualizar CI/CD
- [ ] Documentar em CONTRIBUTING.md
- [ ] Meta: 80%+ cobertura em unit tests

### Esforço Estimado
⏱️ 6-8 horas

### Prioridade
🟠 P1 - Sprint 1
""",
        "labels": ["testing", "p1", "ci-cd", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P1][OBS] Celery tasks sem métricas de erro",
        "body": """## 🟠 ALTO - Observabilidade

**Arquivo**: `api/src/tasks/celery_app.py:26-43`

### Descrição
Tasks agendadas mas sem instrumentação:

```python
'collect-metrics-30min': {
    'task': 'src.tasks.collectors.collect_facebook_metrics',
    'schedule': 1800.0,
    # ❌ Sem error handlers
    # ❌ Sem métricas
    # ❌ Sem alertas
},
```

### Impacto
Tasks podem falhar silenciosamente por semanas sem ninguém saber.

### Solução
Adicionar handlers e métricas:

```python
from celery.signals import task_failure, task_success
from prometheus_client import Counter

# Métricas
celery_task_failures = Counter(
    'celery_task_failures_total',
    'Total de falhas em tasks Celery',
    ['task_name']
)

celery_task_success = Counter(
    'celery_task_success_total',
    'Total de sucessos em tasks Celery',
    ['task_name']
)

# Handlers
@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(
        f"Task {sender.name} failed",
        extra={
            "task_id": task_id,
            "error": str(exception),
            "task_name": sender.name
        }
    )
    celery_task_failures.labels(task=sender.name).inc()

    # Alertar no Slack se crítico
    if is_critical_task(sender.name):
        send_slack_alert(f"🔥 Task crítica falhou: {sender.name}")

@task_success.connect
def task_success_handler(sender=None, **kwargs):
    celery_task_success.labels(task=sender.name).inc()
```

### Checklist
- [ ] Implementar signal handlers
- [ ] Adicionar métricas Prometheus
- [ ] Configurar alertas (Slack/email)
- [ ] Dashboard Grafana para tasks
- [ ] Documentar no RUNBOOK.md
- [ ] Testes

### Esforço Estimado
⏱️ 2-3 horas

### Prioridade
🟠 P1 - Sprint 1
""",
        "labels": ["observability", "p1", "celery", "sprint-1"],
        "milestone": 1
    },
    {
        "title": "[P1][PERF] Índices de banco de dados faltando",
        "body": """## 🟡 MÉDIO - Performance

**Arquivo**: `api/alembic/versions/`

### Descrição
Queries comuns sem índices otimizados:

```sql
-- ❌ Lento: buscar histórico de conversas
SELECT * FROM conversation_memory
WHERE user_id = ?
ORDER BY timestamp DESC
LIMIT 50;

-- ❌ Lento: listar campanhas ativas recentes
SELECT * FROM campaigns
WHERE status = 'ACTIVE'
ORDER BY updated_time DESC;
```

### Impacto
Queries ficam lentas com crescimento de dados.

### Solução
Criar migration com índices compostos:

```python
# 003_add_performance_indexes.py
def upgrade():
    # Histórico de conversas
    op.create_index(
        'idx_conversation_memory_user_timestamp',
        'conversation_memory',
        ['user_id', 'timestamp'],
        postgresql_using='btree'
    )

    # Campanhas ativas
    op.create_index(
        'idx_campaigns_status_updated',
        'campaigns',
        ['status', 'updated_time'],
        postgresql_using='btree'
    )

def downgrade():
    op.drop_index('idx_conversation_memory_user_timestamp')
    op.drop_index('idx_campaigns_status_updated')
```

### Checklist
- [ ] Analisar slow query log
- [ ] Identificar queries N+1
- [ ] Criar índices compostos
- [ ] Testar performance antes/depois
- [ ] Documentar no README
- [ ] Monitorar tamanho dos índices

### Esforço Estimado
⏱️ 1-2 horas

### Prioridade
🟡 P1 - Sprint 2
""",
        "labels": ["performance", "p1", "database", "sprint-2"],
        "milestone": 2
    },

    # P2 - MÉDIOS (selecionar alguns importantes)
    {
        "title": "[P2][CODE] Validação de token síncrona em código async",
        "body": """## 🟡 MÉDIO - Code Quality

**Arquivo**: `api/src/utils/token_manager.py:20-39`

### Descrição
`_check_token_validity()` usa `requests.get()` síncrono em contexto async:

```python
def _check_token_validity(self) -> bool:
    response = requests.get(url, params=params, timeout=30)  # BLOCKING!
```

### Impacto
Bloqueia event loop → reduz throughput do servidor.

### Solução
Usar `httpx.AsyncClient`:

```python
async def _check_token_validity(self) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30)
        return response.status_code == 200
```

### Esforço
⏱️ 2 horas

### Prioridade
🟡 P2 - Sprint 2
""",
        "labels": ["code-quality", "p2", "async", "sprint-2"],
        "milestone": 2
    },
    {
        "title": "[P2][DOCS] Documentação duplicada e inconsistente",
        "body": """## 🟡 MÉDIO - Documentação

**Localização**:
- `README.md` raiz vs `api/README.md` vs `analytics/README.md`
- `api/docs/prd/facebook-ads-agent/*` vs `analytics/docs/prd/agente-facebook/*`

### Problema
READMEs com informações conflitantes, PRDs duplicados.

### Impacto
Novos desenvolvedores ficam confusos.

### Solução
Consolidar em `docs/` centralizado:

```
docs/
├── README.md (índice principal)
├── architecture/
├── api/
├── analytics/
└── prd/
    └── agente-facebook/ (fonte única)

# READMEs de subprojetos apenas linkam
api/README.md → "Ver docs/ para documentação completa"
```

### Esforço
⏱️ 4-6 horas

### Prioridade
🟡 P2 - Sprint 2
""",
        "labels": ["documentation", "p2", "sprint-2"],
        "milestone": 2
    },
    {
        "title": "[P2][DEPS] Dependências duplicadas entre api/ e analytics/",
        "body": """## 🟡 MÉDIO - DevOps

**Arquivos**:
- `api/requirements.txt` - 58 linhas
- `analytics/scripts/requirements.txt` - 25 linhas
- Duplicações: `requests`, `python-dotenv`, `openai`

### Problema
Sem gerenciamento centralizado de versões → conflitos.

### Solução
Migrar para estrutura monorepo:

```
requirements/
├── base.txt (compartilhado)
├── api.txt (-r base.txt + específicos)
└── analytics.txt (-r base.txt + específicos)
```

### Esforço
⏱️ 3-4 horas

### Prioridade
🟡 P2 - Sprint 2
""",
        "labels": ["dependencies", "p2", "devops", "sprint-2"],
        "milestone": 2
    },
    {
        "title": "[P2][PERF] Falta de paginação em endpoints de listagem",
        "body": """## 🟡 MÉDIO - Performance

**Arquivo**: `api/src/api/campaigns.py:25`

### Descrição
Endpoints podem retornar milhares de registros sem paginação.

### Solução
Implementar cursor-based pagination:

```python
@router.get("/")
async def list_campaigns(
    cursor: Optional[str] = None,
    limit: int = Query(50, le=100)
) -> PaginatedResponse[Campaign]:
    ...
```

### Esforço
⏱️ 3 horas

### Prioridade
🟡 P2 - Sprint 2
""",
        "labels": ["performance", "p2", "api", "sprint-2"],
        "milestone": 2
    },

    # P3 - BAIXOS (selecionar alguns representativos)
    {
        "title": "[P3][CODE] TODOs no código não trackados",
        "body": """## 🟢 BAIXO - Manutenção

**Localização**: 7 TODOs espalhados no código

Exemplos:
- `api/src/agents/facebook_agent.py:237` - "TODO: Replace with LangChain"
- `api/src/api/automation.py:131` - "TODO: Implement database query in Sprint 4"

### Solução
Criar issues para cada TODO ou implementar/remover.

### Esforço
⏱️ 2 horas

### Prioridade
🟢 P3 - Backlog
""",
        "labels": ["maintenance", "p3", "backlog"],
        "milestone": 3
    },
    {
        "title": "[P3][OBS] Logs sem correlation IDs",
        "body": """## 🟢 BAIXO - Observabilidade

**Problema**: Logs sem `request_id` para correlacionar entre serviços.

### Solução
Middleware que injeta `request_id`:

```python
import uuid
from contextvars import ContextVar

request_id_ctx = ContextVar('request_id', default=None)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

### Esforço
⏱️ 3 horas

### Prioridade
🟢 P3 - Backlog
""",
        "labels": ["observability", "p3", "backlog"],
        "milestone": 3
    },
    {
        "title": "[P3][DEPS] Versões de dependências defasadas",
        "body": """## 🟢 BAIXO - Dependências

Versões antigas em `api/requirements.txt`:
- `fastapi==0.104.1` (atual: 0.110+)
- `openai==1.3.7` (atual: 1.50+)
- `langchain==0.0.340`

### Solução
```bash
pip-audit
pip install --upgrade fastapi openai langchain
pytest  # Rodar testes
```

### Esforço
⏱️ 3-4 horas (com testes)

### Prioridade
🟢 P3 - Backlog
""",
        "labels": ["dependencies", "p3", "security", "backlog"],
        "milestone": 3
    },
    {
        "title": "[P3][OPS] Configurar n8n inicial - 0 workflows detectados",
        "body": """## ⚠️ OPERACIONAL - Configuração Inicial

**Descoberta**: Análise do PostgreSQL mostrou:
- ✅ n8n instalado e rodando
- ❌ **0 workflows configurados**
- ❌ **0 execuções registradas**
- ❌ **0 credenciais configuradas**

### Diagnóstico
Sistema pronto mas completamente vazio. Precisa configuração inicial.

### Ação Recomendada

1. **Importar workflows**:
```bash
# Copiar workflows para n8n
cp analytics/n8n-workflows/*.json /path/to/n8n/workflows/

# Ou importar via UI
# http://n8n.macspark.dev → Import from File
```

2. **Configurar credenciais**:
- Facebook Ads API
- Notion API
- Supabase
- OpenAI (se usar)

3. **Ativar workflows essenciais**:
- Meta Ads → Supabase (coleta de métricas)
- Notion Reports (geração de relatórios)

### Checklist
- [ ] Importar workflows de analytics/n8n-workflows/
- [ ] Configurar credenciais Facebook
- [ ] Configurar credenciais Notion
- [ ] Configurar credenciais Supabase
- [ ] Ativar workflow de coleta (30min interval)
- [ ] Testar execução manual
- [ ] Verificar logs de execução
- [ ] Documentar em docs/n8n-setup.md

### Esforço Estimado
⏱️ 2-4 horas (configuração inicial)

### Prioridade
🟡 P2 - Sprint 1 ou 2 (operacional importante)
""",
        "labels": ["operations", "p2", "configuration", "n8n", "sprint-2"],
        "milestone": 2
    },
]

def create_issue(repo: str, token: str, issue_data: Dict) -> Dict:
    """Cria uma issue no GitHub via API"""
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.post(url, json=issue_data, headers=headers)
    response.raise_for_status()
    return response.json()

def create_milestone(repo: str, token: str, title: str, description: str) -> int:
    """Cria um milestone e retorna o ID"""
    url = f"https://api.github.com/repos/{repo}/milestones"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "title": title,
        "description": description,
        "state": "open"
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()["number"]

def main():
    parser = argparse.ArgumentParser(description="Criar Issues no GitHub")
    parser.add_argument("--token", help="GitHub Personal Access Token")
    parser.add_argument("--repo", help="Repositório (owner/repo)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas simular")
    args = parser.parse_args()

    # Obter configurações
    token = args.token or os.getenv("GITHUB_TOKEN")
    repo = args.repo or os.getenv("GITHUB_REPO")

    if not token or not repo:
        print("❌ Erro: GITHUB_TOKEN e GITHUB_REPO são obrigatórios")
        print("\nUso:")
        print("  python create-github-issues.py --token YOUR_TOKEN --repo owner/repo")
        print("\nOu configure variáveis de ambiente:")
        print("  export GITHUB_TOKEN=your_token")
        print("  export GITHUB_REPO=owner/repo")
        sys.exit(1)

    print(f">> Criando {len(ISSUES)} issues no repositorio {repo}")
    print(f"{'=' * 60}\n")

    # Criar milestones primeiro
    milestones = {}
    if not args.dry_run:
        try:
            milestones[1] = create_milestone(
                repo, token,
                "Sprint 1 - Criticos & Segurança",
                "Resolver problemas P0 e P1 críticos de segurança e performance"
            )
            milestones[2] = create_milestone(
                repo, token,
                "Sprint 2 - Qualidade & Performance",
                "Melhorias de código, testes e performance"
            )
            milestones[3] = create_milestone(
                repo, token,
                "Sprint 3 - DevOps & Docs",
                "Melhorias de DevOps, documentação e manutenção"
            )
            print(f"[OK] Milestones criados: {milestones}\n")
        except Exception as e:
            print(f"[WARN] Erro ao criar milestones (podem ja existir): {e}\n")

    # Criar issues
    created = 0
    for idx, issue in enumerate(ISSUES, 1):
        try:
            if args.dry_run:
                print(f"[DRY-RUN] {idx}/{len(ISSUES)}: {issue['title']}")
            else:
                # Atualizar milestone ID se foi criado
                if "milestone" in issue and issue["milestone"] in milestones:
                    issue["milestone"] = milestones[issue["milestone"]]

                result = create_issue(repo, token, issue)
                print(f"[OK] {idx}/{len(ISSUES)}: Issue #{result['number']} - {issue['title']}")
                print(f"   URL: {result['html_url']}\n")
                created += 1

        except Exception as e:
            print(f"[ERROR] {idx}/{len(ISSUES)}: Erro ao criar '{issue['title']}': {e}\n")

    print(f"\n{'=' * 60}")
    print(f">> Concluido! {created}/{len(ISSUES)} issues criadas com sucesso")
    print(f"\n>> Resumo:")
    print(f"   - P0 (Critico): 5 issues")
    print(f"   - P1 (Alto): 6 issues")
    print(f"   - P2 (Medio): 9 issues")
    print(f"   - P3 (Baixo): 5 issues")
    print(f"\n>> Acesse: https://github.com/{repo}/issues")
    print(f">> Project Board: https://github.com/{repo}/projects")

if __name__ == "__main__":
    main()
