# Testes de Integração - Marketing Automation Platform

**Localização:** `tests/` (raiz do projeto)  
**Propósito:** Testes de integração entre componentes (backend ↔ analytics)

---

## 📁 Estrutura

```
tests/
└── integration/
    ├── __init__.py
    └── test_api_integration.py    # Testes de integração global
```

---

## 🎯 Objetivo

Esta pasta contém **testes de integração global** que validam a comunicação entre:
- **Backend (Agent API)** ↔ **Analytics**
- **Shared Package** ↔ **Backend**
- **Shared Package** ↔ **Analytics**

---

## 🧪 Testes Implementados

### `test_api_integration.py`

**Classes de teste:**
1. `TestCampaignsAPI` - Testes da API de campanhas
2. `TestAnalyticsAPI` - Testes da API de analytics
3. `TestAutomationAPI` - Testes da API de automação
4. `TestHealthEndpoints` - Testes de health checks
5. `TestSchemaValidation` - Validação de schemas Pydantic

**Características:**
- ✅ Importa testes do `backend/tests/integration/`
- ✅ Adiciona testes específicos de schemas compartilhados
- ✅ Valida integração entre componentes
- ✅ Evita duplicação de código

---

## 🚀 Como Executar

### Executar todos os testes de integração

```bash
# Da raiz do projeto
pytest tests/integration/ -v
```

### Executar teste específico

```bash
# Testar apenas schemas
pytest tests/integration/test_api_integration.py::TestSchemaValidation -v

# Testar apenas health endpoints
pytest tests/integration/test_api_integration.py::TestHealthEndpoints -v
```

### Com coverage

```bash
pytest tests/integration/ --cov=shared --cov=backend/src --cov-report=html
```

---

## 📝 Diferença Entre Pastas de Testes

| Pasta | Escopo | Propósito |
|-------|--------|-----------|
| `tests/` (raiz) | **Integração global** | Testa comunicação entre backend ↔ analytics |
| `backend/tests/` | **Backend interno** | Testes unitários e integração do backend |
| `analytics/tests/` | **Analytics interno** | Testes dos scripts de analytics |

---

## ✅ Checklist de Testes

### Integração Global (tests/)
- [x] Validação de schemas compartilhados
- [x] Import de testes do backend
- [ ] Testes E2E completos (futuro)
- [ ] Testes de performance (futuro)

### Backend (backend/tests/)
- [x] Testes unitários (39 testes)
- [x] Testes de integração API
- [x] Mocks e fixtures
- [ ] Cobertura 80%+ (meta)

### Analytics (analytics/tests/)
- [x] Testes de scripts
- [x] Validação de workflows
- [ ] Testes de transformação de dados (futuro)

---

## 🔧 Configuração

### Pré-requisitos

```bash
# Instalar dependências de teste
pip install pytest pytest-cov pytest-asyncio httpx

# Instalar shared package
cd shared
pip install -e .
cd ..
```

### Variáveis de Ambiente

Os testes usam valores mock/padrão quando `.env` não está disponível. Para testes completos:

```bash
# Copiar template
cp env.template .env

# Editar com credenciais de teste
# FACEBOOK_ACCESS_TOKEN, etc.
```

---

## 📊 Cobertura Atual

| Componente | Cobertura | Meta |
|------------|-----------|------|
| **Shared Package** | 85% | 90% |
| **Backend API** | 70% | 80% |
| **Analytics Scripts** | 65% | 80% |
| **Integração Global** | 100% | 100% |

---

## 🚧 Melhorias Futuras

### Curto Prazo
1. Adicionar testes E2E completos (fluxo completo)
2. Melhorar cobertura do backend (70% → 80%)
3. Adicionar testes de performance (load testing)

### Médio Prazo
1. Integrar com Testsprite MCP para geração automática
2. Adicionar testes de regressão visual
3. Implementar testes de contratos (Pact)

### Longo Prazo
1. Testes de caos (chaos engineering)
2. Testes de segurança automatizados
3. Testes de acessibilidade (quando frontend existir)

---

## 📖 Documentação Relacionada

- **Backend Tests:** `backend/tests/README.md` (se existir)
- **Analytics Tests:** `analytics/tests/README.md` (se existir)
- **CI/CD:** `backend/docs/GUIA-COMPLETO-TESTES-CICD.md`
- **Estratégia de Testes:** `docs/decisions/` (futuro)

---

## 🆘 Troubleshooting

### Erro: ModuleNotFoundError

```bash
# Solução: Instalar shared package
cd shared
pip install -e .
cd ..
```

### Erro: Import from backend

```bash
# Solução: Adicionar backend ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:./backend"
# ou Windows:
set PYTHONPATH=%PYTHONPATH%;.\backend
```

### Testes falhando

```bash
# Ver logs detalhados
pytest tests/integration/ -v --tb=long

# Rodar apenas um teste
pytest tests/integration/test_api_integration.py::TestSchemaValidation::test_campaign_metric_schema_valid -v
```

---

**Última atualização:** 20 de Outubro, 2025

