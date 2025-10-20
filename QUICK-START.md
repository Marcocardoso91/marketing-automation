# Quick Start - Marketing Automation Platform

Guia rápido para começar a usar o sistema integrado.

## ⚡ Início Rápido (15 minutos)

### 1. Configurar Ambiente

```powershell
cd C:\Users\marco\Macspark\marketing-automation

# Copiar template de configuração
Copy-Item env.template .env

# Gerar API keys
function Generate-Key {
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    [Convert]::ToBase64String($bytes) -replace '[/+=]', ''
}

Write-Host "Cole no .env:"
Write-Host "ANALYTICS_API_KEY=$(Generate-Key)"
Write-Host "SECRET_KEY=$(Generate-Key)"
Write-Host "SUPERSET_SECRET_KEY=$(Generate-Key)"
```

### 2. Editar .env

Abra `.env` e configure:
```bash
# Obrigatório
FACEBOOK_ACCESS_TOKEN=seu_token_aqui
FACEBOOK_AD_ACCOUNT_ID=act_123456789
ANALYTICS_API_KEY=chave_gerada_acima
SECRET_KEY=chave_gerada_acima

# Recomendado
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_KEY=sua_service_key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### 3. Executar Setup

```powershell
.\scripts\setup.ps1
```

Este script irá:
- ✅ Instalar pacote shared
- ✅ Criar redes Docker
- ✅ Build containers
- ✅ Inicializar PostgreSQL

### 4. Subir Serviços

```bash
docker-compose -f docker-compose.integrated.yml up -d
```

Aguarde ~2 minutos para todos os serviços iniciarem.

### 5. Validar

```powershell
# Health check
.\scripts\health-check.ps1

# Validação completa
python scripts\validate-integration.py
```

### 6. Acessar

- **Agent API (Swagger):** http://localhost:8000/docs
- **Apache Superset:** http://localhost:8088
  - User: admin
  - Pass: (veja .env SUPERSET_ADMIN_PASSWORD)

## ✅ Validação Rápida

### Teste 1: Agent API está UP?

```bash
curl http://localhost:8000/health
```

**Esperado:** `{"status":"healthy","version":"1.0.0","environment":"production"}`

### Teste 2: Endpoint de métricas responde?

```bash
curl http://localhost:8000/api/v1/metrics/health
```

**Esperado:** `{"status":"healthy","endpoint":"metrics","version":"1.0.0"}`

### Teste 3: Autenticação funciona?

```bash
curl http://localhost:8000/api/v1/metrics/export?date_from=2025-10-18&date_until=2025-10-18
```

**Esperado:** 401 Unauthorized ou 422 Validation Error (sem header X-API-Key)

### Teste 4: Pacote shared importa?

```bash
python -c "from marketing_shared.utils.api_client import AgentAPIClient; print('✅ OK')"
```

**Esperado:** `✅ OK`

## 🐛 Problemas Comuns

### Docker não inicia

```bash
# Verificar se Docker está rodando
docker ps

# Iniciar Docker Desktop (Windows)
# Tentar novamente
```

### Porta 8000 em uso

```bash
# Ver o que está usando a porta
netstat -ano | findstr :8000

# Parar o processo ou mudar a porta no docker-compose.integrated.yml
```

### Pacote shared não encontrado

```bash
cd shared
pip install -e .
cd ..
```

## 📚 Próximos Passos

1. ✅ Leia [README.md](README.md) para visão completa
2. ✅ Configure workflows n8n (veja Analytics docs)
3. ✅ Crie dashboards no Superset
4. ✅ Teste fluxo completo end-to-end

## 🆘 Ajuda

- **Integração:** [docs/INTEGRATION-GUIDE.md](docs/INTEGRATION-GUIDE.md)
- **Arquitetura:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Migração:** [MIGRATION.md](MIGRATION.md)
- **Checklist:** [VALIDATION-CHECKLIST.md](VALIDATION-CHECKLIST.md)

---

**Tempo Total:** ~15 minutos  
**Dificuldade:** Fácil  
**Pré-requisito:** Docker + Python 3.12+

