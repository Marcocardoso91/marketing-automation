# 🚀 COMO EXECUTAR O PROJETO

Guia rápido para rodar o Facebook Ads AI Agent localmente ou em produção.

---

## ✅ PRÉ-REQUISITOS

### Software
- ✅ Python 3.11+ instalado
- ✅ Docker Desktop instalado e rodando (Windows)
- ✅ Git instalado

### Credenciais Facebook
Você precisará de:
1. Facebook App ID
2. Facebook App Secret
3. Facebook Access Token
4. Facebook Ad Account ID (formato: `act_123456789`)

**Como obter:** https://developers.facebook.com/apps/

---

## 🎯 OPÇÃO 1: RODAR SEM DOCKER (Desenvolvimento)

### Passo 1: Instalar Dependências

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Configurar .env

```powershell
# Copiar template
copy .env.example .env

# Editar .env com suas credenciais
notepad .env
```

**Configurar no mínimo:**
```bash
FACEBOOK_APP_ID=seu_app_id_aqui
FACEBOOK_APP_SECRET=seu_app_secret_aqui
FACEBOOK_ACCESS_TOKEN=seu_token_aqui
FACEBOOK_AD_ACCOUNT_ID=act_123456789
```

### Passo 3: Rodar Aplicação

```powershell
# Executar
python main.py

# Ou com reload automático
uvicorn main:app --reload
```

### Passo 4: Testar

```powershell
# Em outro terminal
curl http://localhost:8000/health
# Esperado: {"status":"healthy","version":"1.0.0","environment":"development"}

# Acessar Swagger UI
# Navegador: http://localhost:8000/docs
```

---

## 🐳 OPÇÃO 2: RODAR COM DOCKER (Recomendado)

### Passo 1: Configurar .env

```powershell
copy .env.example .env
notepad .env
```

**Configure suas credenciais Facebook**

### Passo 2: Build e Start

```powershell
# Build das imagens
docker-compose build

# Iniciar todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps
```

**Serviços que devem estar UP:**
- ✅ fbads-api (porta 8000)
- ✅ fbads-celery-worker
- ✅ fbads-celery-beat
- ✅ fbads-flower (porta 5555)
- ✅ fbads-postgres (porta 5432)
- ✅ fbads-redis (porta 6379)
- ✅ fbads-n8n (porta 5678)
- ✅ fbads-prometheus (porta 9090)
- ✅ fbads-grafana (porta 3000)

### Passo 3: Rodar Migrations

```powershell
# Executar migrations do banco
docker-compose exec app alembic upgrade head
```

### Passo 4: Testar

```powershell
# Health check
curl http://localhost:8000/health

# Listar campanhas
curl http://localhost:8000/api/v1/campaigns

# Acessar interfaces
```

**Abrir no navegador:**
- API Swagger: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- n8n: http://localhost:5678 (admin/admin)
- Flower (Celery): http://localhost:5555
- Prometheus: http://localhost:9090

---

## 📊 TESTAR APIs

### 1. Health Check

```powershell
curl http://localhost:8000/health
```

**Esperado:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Listar Campanhas

```powershell
curl http://localhost:8000/api/v1/campaigns?status=ACTIVE
```

**Esperado:** Lista de campanhas ativas do Facebook Ads

### 3. Dashboard Analytics

```powershell
curl http://localhost:8000/api/v1/analytics/dashboard
```

**Esperado:** 
```json
{
  "summary": {
    "total_spend": 1234.56,
    "total_clicks": 500,
    "average_ctr": 2.5,
    ...
  },
  "top_campaigns": [...]
}
```

### 4. Análise de Performance

```powershell
curl http://localhost:8000/api/v1/analytics/performance
```

**Esperado:** Campanhas com scores 0-100

### 5. Sugestões de Pausa

```powershell
curl -X POST http://localhost:8000/api/v1/automation/pause-underperforming `
  -H "Content-Type: application/json" `
  -d "{\"ctr_threshold\": 1.0, \"cpa_threshold\": 50.0}"
```

**Esperado:** Lista de campanhas sugeridas para pausa com reasoning

### 6. Chat (Linguagem Natural)

```powershell
curl -X POST http://localhost:8000/api/v1/chat `
  -H "Content-Type: application/json" `
  -d "{\"message\": \"Liste campanhas ativas\"}"
```

**Esperado:**
```json
{
  "type": "campaigns_list",
  "query": "Liste campanhas ativas",
  "data": [...]
}
```

---

## 🧪 RODAR TESTES

```powershell
# Todos os testes
pytest tests/

# Apenas unitários
pytest tests/unit/

# Apenas integração
pytest tests/integration/

# Com coverage
pytest --cov=src --cov-report=html
# Relatório em: htmlcov/index.html
```

---

## 🔧 COMANDOS ÚTEIS (Makefile)

```powershell
# Instalar dependências
make install

# Testes
make test
make test-unit
make test-integration

# Lint e format
make lint
make format

# Docker
make docker-build
make docker-up
make docker-down
make docker-logs

# Database migrations
make migrate
make migrate-rollback

# Security scan
make security-scan
```

---

## 📈 MONITORAR APLICAÇÃO

### Ver Logs

```powershell
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f app

# Apenas Celery
docker-compose logs -f celery_worker
```

### Métricas Prometheus

Acessar: http://localhost:9090

**Queries úteis:**
```promql
# Taxa de requests
rate(api_requests_total[5m])

# Latência p95
histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))

# Campanhas ativas
active_campaigns
```

### Dashboards Grafana

Acessar: http://localhost:3000 (admin/admin)

1. Configurar datasource Prometheus (já deve estar configurado)
2. Importar ou criar dashboards

---

## 🛑 PARAR APLICAÇÃO

### Sem Docker

```powershell
# Ctrl+C no terminal onde está rodando python main.py
```

### Com Docker

```powershell
# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: perde dados!)
docker-compose down -v
```

---

## 🔥 TROUBLESHOOTING

### Erro: Port already in use

```powershell
# Verificar quem está usando a porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Erro: Cannot connect to Docker daemon

**Solução:** Certifique-se de que Docker Desktop está rodando

### Erro: ModuleNotFoundError

```powershell
# Adicionar ao PYTHONPATH
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"

# Ou reinstalar dependências
pip install -r requirements.txt
```

### Erro: Facebook API - Invalid token

**Solução:**
1. Gerar novo token: https://developers.facebook.com/tools/accesstoken/
2. Atualizar no .env
3. Reiniciar aplicação

---

## 📚 DOCUMENTAÇÃO

### Arquitetura e Planejamento
- [README-AUDITORIA.md](README-AUDITORIA.md) - Resumo executivo da auditoria
- [docs/auditoria/](docs/auditoria/) - Documentação técnica completa (6 docs)

### Operacional
- [docs/RUNBOOK.md](docs/RUNBOOK.md) - Guia de operações e emergências
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Guia de deploy em produção
- [docs/n8n-setup.md](docs/n8n-setup.md) - Configuração workflows n8n
- [docs/GUIA-COMPLETO-TESTES-CICD.md](docs/GUIA-COMPLETO-TESTES-CICD.md) - Testes e CI/CD

### Código
- [README.md](README.md) - Documentação principal do projeto
- [CHANGELOG.md](CHANGELOG.md) - Histórico de mudanças
- [STATUS-PROJETO.md](STATUS-PROJETO.md) - Status atual da implementação

---

## 🎉 PRÓXIMOS PASSOS

Depois de rodar localmente com sucesso:

1. ✅ **Testar todos endpoints** no Swagger UI
2. ✅ **Configurar workflows n8n** (ver docs/n8n-setup.md)
3. ✅ **Visualizar métricas** no Grafana
4. ⏳ **Implementar testes unitários atualizados**
5. ⏳ **Deploy em staging**
6. ⏳ **Deploy em produção** (ver docs/DEPLOYMENT.md)

---

**Sucesso na execução! 🚀**

**Dúvidas?** Consulte a documentação em `/docs/`


