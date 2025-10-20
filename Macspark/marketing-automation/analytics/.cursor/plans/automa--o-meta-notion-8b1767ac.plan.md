<!-- 8b1767ac-6902-4a0c-8c49-c62c339b3857 4f3c7568-e47e-49bb-bb38-44ddae2507d6 -->
# Plano de Finalizacao e Correcao - Agente Facebook v3.0.0

## Escopo

Implementar 9 tarefas criticas (P0) e importantes (P1) para levar o projeto de 78.7/100 para 95+/100 em qualidade de codigo, com testes completos, type hints, linting, e documentacao atualizada.

## Fase 1: Validacao e Setup (20 min)

### 1.1 Validar Dependencias Python Instaladas

- Verificar se pytest, pylint, black, mypy ja estao instalados
- Se nao: instalar via `pip install -r scripts/requirements-dev.txt` (a ser criado)
- Validar versao Python (deve ser 3.12)

### 1.2 Criar Estrutura de Testes

- Criar diretorio `tests/` na raiz
- Criar `tests/__init__.py`
- Criar `tests/conftest.py` com fixtures de setup de ambiente

## Fase 2: Testes Completos (2-3 horas)

### 2.1 Criar Suite de Testes Unitarios

**Arquivo:** `tests/test_metrics_to_supabase.py` (~350 linhas)

Classes de teste a criar:

- `TestMetaAdsIntegration`: 5 testes (coleta, erro API, processamento, calculos)
- `TestYouTubeIntegration`: 3 testes (coleta, erro, processamento)
- `TestGoogleAnalyticsIntegration`: 2 testes (placeholder, erro)
- `TestGoogleAdsIntegration`: 2 testes (placeholder, erro)
- `TestSupabaseIntegration`: 4 testes (save, upsert, consolidate, erro)
- `TestOpenAIIntegration`: 3 testes (insights, erro, formato)
- `TestSlackIntegration`: 2 testes (notificacao simples, rica)

Usar `unittest.mock` para mockar requests, supabase client, openai client.

### 2.2 Criar Testes para meta-to-notion.py

**Arquivo:** `tests/test_meta_to_notion.py` (~150 linhas)

- Testar `get_meta_ads_metrics()`
- Testar `send_to_notion()`
- Testar calculo de metricas agregadas

### 2.3 Configurar pytest

**Arquivo:** `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --verbose --cov=scripts --cov-report=html --cov-report=term-missing --cov-fail-under=70
```

**Meta:** Coverage >= 70%

## Fase 3: Type Hints Completos (1-1.5 horas)

### 3.1 Adicionar Type Hints em metrics-to-supabase.py

Funcoes a tipar (13 funcoes):

- `get_meta_ads_metrics(date_preset: str) -> Optional[List[Dict[str, Any]]]`
- `get_youtube_metrics() -> Optional[Dict[str, Any]]`
- `get_google_analytics_metrics() -> Optional[Dict[str, Any]]`
- `get_google_ads_metrics() -> Optional[Dict[str, Any]]`
- `process_meta_ads(campaigns_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]`
- `process_youtube(stats_data: Dict[str, Any]) -> Optional[Dict[str, Any]]`
- `save_to_supabase(metrics: Dict[str, Any]) -> bool`
- `consolidate_metrics(date_str: str) -> Optional[Dict[str, Any]]`
- `generate_insights_openai(consolidated: Dict[str, Any]) -> str`
- `send_slack_notification(consolidated: Dict[str, Any], ai_insight: str) -> bool`
- `main() -> None`

Imports necessarios: `from typing import Optional, List, Dict, Any`

### 3.2 Adicionar Type Hints em meta-to-notion.py

Funcoes a tipar (5 funcoes):

- `get_meta_ads_metrics(date_preset: str) -> Optional[List[Dict[str, Any]]]`
- `send_to_notion(metrics: Dict[str, Any]) -> bool`
- `calculate_aggregates(campaigns: List[Dict[str, Any]]) -> Dict[str, Any]`
- `format_for_notion(data: Dict[str, Any]) -> Dict[str, Any]`
- `main() -> None`

### 3.3 Adicionar Type Hints em superset_config.py

- Tipar variaveis de configuracao
- Adicionar docstrings

## Fase 4: Linting e Formatting (30 min)

### 4.1 Criar requirements-dev.txt

**Arquivo:** `scripts/requirements-dev.txt`

```
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
pylint==3.0.3
black==23.12.1
flake8==6.1.0
mypy==1.7.1
types-requests==2.31.0.10
```

### 4.2 Criar pyproject.toml

**Arquivo:** `pyproject.toml` (raiz)

Configurar:

- [tool.black]: line-length=100, target-version=py312
- [tool.pylint]: max-line-length=100, disable warnings menores
- [tool.mypy]: python_version=3.12, warn_return_any=true, ignore_missing_imports=true
- [tool.pytest.ini_options]: testpaths, coverage

### 4.3 Formatar Codigo

- Executar `black scripts/` para formatar todos os arquivos Python
- Executar `pylint scripts/*.py` para validar score >= 8.0
- Executar `mypy scripts/` para validar type hints

## Fase 5: Validacao de Ambiente (20 min)

### 5.1 Criar Script de Validacao (Windows)

**Arquivo:** `scripts/validate-env.py` (~80 linhas)

Validar variaveis obrigatorias:

- SUPABASE_URL, SUPABASE_SERVICE_KEY
- META_ACCESS_TOKEN, META_AD_ACCOUNT_ID

Validar variaveis opcionais (warning):

- GA4_PROPERTY_ID, GOOGLE_ADS_CUSTOMER_ID
- YOUTUBE_CHANNEL_ID, YOUTUBE_API_KEY
- OPENAI_API_KEY, SLACK_WEBHOOK_URL

Retornar exit code 0 se OK, 1 se faltando variaveis obrigatorias.

### 5.2 Criar Script Bash (para Linux/Mac)

**Arquivo:** `scripts/validate-env.sh` (~40 linhas)

Mesma logica que o Python, mas em bash.

## Fase 6: Gitignore e Seguranca (10 min)

### 6.1 Criar .gitignore Completo

**Arquivo:** `.gitignore` (raiz, ~50 linhas)

Ignorar:

- Python: `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, `htmlcov/`, `.coverage`
- Environment: `.env`, `.env.local`, `*.env`
- IDE: `.vscode/`, `.idea/`, `.cursor/`
- OS: `.DS_Store`, `Thumbs.db`
- Logs: `*.log`, `logs/`
- Docker: `docker-compose.override.yml`
- Sensitive: `notion_tokens.json`, `credentials.json`

## Fase 7: Atualizacao de Documentacao (1 hora)

### 7.1 Atualizar PRD.en-US.md

**Arquivo:** `docs/prd/agente-facebook/PRD.en-US.md`

Traducoes e atualizacoes necessarias:

- Versao: 2.0.0 -> 3.0.0
- Adicionar RF-011 a RF-015 (5 novos requisitos funcionais)
- Adicionar RNF-008 a RNF-010 (3 novos requisitos nao-funcionais)
- Atualizar secao "Architecture" com stack completo (Supabase, Superset, OpenAI, Slack)
- Adicionar ADR-010 a ADR-013 na secao "Decisions"
- Atualizar tabela de integracao (5 fontes de dados)

Ref: Usar `PRD.pt-BR.md` como base (ja atualizado para v3.0.0)

### 7.2 Atualizar backlog.csv

**Arquivo:** `docs/prd/agente-facebook/backlog.csv`

Adicionar 20 novos itens (BACK-045 a BACK-064):

- BACK-045 a BACK-051: Features v3.0.0 (Done)
- BACK-052 a BACK-055: Tasks P0/P1 (Todo/In Progress)
- BACK-056 a BACK-059: Tasks P2, Docs (Todo)
- BACK-060 a BACK-064: Features futuras (Backlog)

Campos: ID, Tipo, Prioridade, Status, Titulo, Descricao, Estimativa

## Fase 8: Execucao e Validacao (30 min)

### 8.1 Instalar Dependencias de Dev

```bash
cd scripts/
pip install -r requirements-dev.txt
```

### 8.2 Validar Ambiente

```bash
python scripts/validate-env.py
```

### 8.3 Executar Testes

```bash
pytest tests/ -v --cov=scripts --cov-report=html
```

Meta: Passar todos os testes, coverage >= 70%

### 8.4 Executar Linting

```bash
black scripts/ --check
pylint scripts/*.py
mypy scripts/
```

Meta: Black OK, Pylint >= 8.0, Mypy 0 errors

### 8.5 Gerar Relatorio HTML de Coverage

```bash
# Abrir htmlcov/index.html no navegador
start htmlcov/index.html  # Windows
```

## Fase 9: Relatorio Final (15 min)

### 9.1 Criar Relatorio de Correcoes

**Arquivo:** `RELATORIO-CORRECOES-v3.0.md`

Formato:

```markdown
# RELATORIO DE CORRECOES - Agente Facebook v3.0.0

## STATUS GERAL: [Completo/Parcial/Falhou]

### TAREFAS COMPLETADAS:
- Tarefa 1: Suite de Testes (XX testes, XX% coverage)
- Tarefa 2: Type Hints (XX funcoes tipadas)
- ...

### METRICAS FINAIS:
- Coverage: XX%
- Pylint Score: X.X/10
- Mypy Errors: X
- Tests: XX/XX passing

### COMANDOS PARA VALIDACAO:
[comandos para re-executar testes]

### PROBLEMAS ENCONTRADOS:
[se houver]

### PROXIMOS PASSOS RECOMENDADOS:
[Google APIs, OpenAI, etc]
```

## Criterios de Aceitacao

### Obrigatorios (P0):

- [ ] Todos os testes passam (pytest green)
- [ ] Coverage >= 70%
- [ ] Pylint score >= 8.0
- [ ] Black formata sem erros
- [ ] Mypy sem erros criticos
- [ ] Todos os arquivos criados/modificados conforme especificado

### Importantes (P1):

- [ ] PRD.en-US.md atualizado para v3.0.0
- [ ] backlog.csv com 20 novos itens
- [ ] .gitignore completo
- [ ] requirements-dev.txt funcional
- [ ] validate-env.py funcionando

## Arquivos a Criar (15 novos):

1. `tests/__init__.py`
2. `tests/conftest.py`
3. `tests/test_metrics_to_supabase.py`
4. `tests/test_meta_to_notion.py`
5. `pytest.ini`
6. `scripts/requirements-dev.txt`
7. `pyproject.toml`
8. `scripts/validate-env.py`
9. `scripts/validate-env.sh`
10. `.gitignore`
11. `RELATORIO-CORRECOES-v3.0.md`

## Arquivos a Modificar (5 existentes):

1. `scripts/metrics-to-supabase.py` (add type hints)
2. `scripts/meta-to-notion.py` (add type hints)
3. `superset_config.py` (add type hints)
4. `docs/prd/agente-facebook/PRD.en-US.md` (update to v3.0.0)
5. `docs/prd/agente-facebook/backlog.csv` (add 20 items)

## Estimativa Total: 6-7 horas

- Fase 1: 20 min
- Fase 2: 2-3 horas
- Fase 3: 1-1.5 horas
- Fase 4: 30 min
- Fase 5: 20 min
- Fase 6: 10 min
- Fase 7: 1 hora
- Fase 8: 30 min
- Fase 9: 15 min

## Notas Importantes

- NAO modificar logica de negocio existente
- NAO alterar estrutura de pastas (exceto criar tests/)
- NAO remover documentacao existente
- APENAS adicionar testes, type hints, configs e correcoes
- MANTER compatibilidade com codigo existente
- SEGUIR PEP8 e convencoes Python

### To-dos

- [ ] Validar dependencias Python e criar requirements-dev.txt
- [ ] Criar estrutura de testes (tests/, conftest.py, pytest.ini)
- [ ] Implementar suite completa de testes (unitarios + integracao, 70%+ coverage)
- [ ] Adicionar type hints completos em todas as funcoes Python
- [ ] Configurar linting (pyproject.toml, black, pylint, mypy)
- [ ] Criar scripts de validacao de ambiente (validate-env.py e .sh)
- [ ] Criar .gitignore completo com todas as regras necessarias
- [ ] Atualizar PRD.en-US.md e backlog.csv para v3.0.0
- [ ] Executar todos os testes, linting e validacoes finais
- [ ] Gerar relatorio final de correcoes (RELATORIO-CORRECOES-v3.0.md)