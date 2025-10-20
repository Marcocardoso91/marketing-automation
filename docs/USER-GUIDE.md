# 📖 Guia de Uso - Marketing Automation Platform

**Versão:** 1.1.0  
**Última atualização:** 20 de Outubro, 2025

---

## 🎯 Para Que Serve Este Sistema

O Marketing Automation Platform automatiza a coleta e análise de métricas de campanhas de marketing (principalmente Meta Ads / Facebook), permitindo:

- ✅ **Coleta automatizada** de métricas diárias
- ✅ **Armazenamento centralizado** no Supabase
- ✅ **Dashboards BI** no Apache Superset
- ✅ **APIs REST** para integração com outras ferramentas
- ✅ **Workflows N8N** para automação avançada

---

## 🚀 Início Rápido

### 1. Primeira Vez (Setup)

```powershell
# 1. Configurar variáveis de ambiente
cd C:\Users\marco\Macspark\marketing-automation
Copy-Item env.template .env
notepad .env  # Editar com suas credenciais

# 2. Executar setup
.\scripts\setup.ps1

# 3. Subir serviços
docker-compose -f docker-compose.integrated.yml up -d
```

### 2. Verificar Saúde

```powershell
.\scripts\health-check.ps1
```

**Output esperado:**
```
✅ Agent API
✅ Metrics Endpoint
✅ Superset
```

---

## 📊 Uso Diário

### Coletar Métricas Manualmente

```powershell
# Ir para scripts analytics
cd analytics\scripts

# Executar coleta
python metrics-to-supabase.py
```

**O que acontece:**
1. ✅ Script chama backend API
2. ✅ Backend busca métricas do Facebook
3. ✅ Dados validados com Pydantic
4. ✅ Salvos no Supabase
5. ✅ Dashboards atualizados automaticamente

### Ver Dashboards

**Apache Superset:**
- URL: http://localhost:8088
- User: admin
- Pass: (ver SUPERSET_ADMIN_PASSWORD no .env)

**Prometheus (Monitoring):**
- URL: http://localhost:9090
- Métricas: Agent API, PostgreSQL

**Grafana (Opcional):**
- URL: http://localhost:3000
- User: admin
- Pass: (ver GRAFANA_ADMIN_PASSWORD no .env)

### Consultar API

**Swagger UI (Documentação Interativa):**
- URL: http://localhost:8000/docs
- Testar endpoints interativamente
- Ver schemas e exemplos

**Endpoints principais:**
```bash
# Health check
curl http://localhost:8000/health

# Exportar métricas (requer API key)
curl -H "X-API-Key: SEU_ANALYTICS_API_KEY" \
  "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-18&date_until=2025-10-18"
```

---

## 🔧 Operações Comuns

### Iniciar Serviços

```powershell
docker-compose -f docker-compose.integrated.yml up -d
```

### Parar Serviços

```powershell
docker-compose -f docker-compose.integrated.yml down
```

### Ver Logs

```powershell
# Todos serviços
docker-compose -f docker-compose.integrated.yml logs -f

# Apenas backend
docker-compose -f docker-compose.integrated.yml logs -f agent-api

# Últimas 50 linhas
docker-compose -f docker-compose.integrated.yml logs --tail=50
```

### Reiniciar Serviço Específico

```powershell
docker-compose -f docker-compose.integrated.yml restart agent-api
```

### Atualizar Código

```powershell
# 1. Parar serviços
docker-compose -f docker-compose.integrated.yml down

# 2. Rebuild
docker-compose -f docker-compose.integrated.yml build

# 3. Subir novamente
docker-compose -f docker-compose.integrated.yml up -d
```

---

## 🛠️ Troubleshooting

### Facebook API retorna 403

**Sintoma:**
```
Status: 403
Error: Ad account owner has NOT grant ads_management permission
```

**Solução:**
1. Acessar https://business.facebook.com/settings
2. Ir em "Contas" → "Apps" → "Marketing API"
3. Adicionar permissões: ads_management, ads_read, business_management
4. Aguardar ~5 minutos propagação
5. Testar: `python scripts\test-facebook.py`

### Token Facebook expirou

**Sintoma:**
```
Error: Invalid OAuth access token
```

**Solução:**
1. Gerar novo token no Graph API Explorer
2. Converter para longa duração (60 dias)
3. Atualizar FACEBOOK_ACCESS_TOKEN no `.env`
4. Reiniciar containers: `docker-compose restart`

### Docker não inicia

**Sintoma:**
```
Error: Cannot connect to Docker daemon
```

**Solução:**
1. Verificar se Docker Desktop está rodando
2. Reiniciar Docker Desktop
3. Verificar portas em uso: `netstat -ano | findstr :8000`

### Porta em uso

**Sintoma:**
```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solução:**
```powershell
# Ver o que usa a porta
netstat -ano | findstr :8000

# Matar processo (substitua PID)
taskkill /PID numero_pid /F

# Ou mudar porta no docker-compose.integrated.yml
```

### Shared package não encontrado

**Sintoma:**
```
ModuleNotFoundError: No module named 'marketing_shared'
```

**Solução:**
```bash
cd shared
pip install -e .
cd ..
```

### Backend não conecta ao Facebook

**Sintoma:**
```
Error: FacebookRequestError
```

**Verificações:**
1. ✅ Token válido no `.env`?
2. ✅ Account ID correto (act_659480752041234)?
3. ✅ Permissões configuradas?
4. ✅ Token não expirou?

### Analytics não salva no Supabase

**Sintoma:**
```
Error connecting to Supabase
```

**Verificações:**
1. ✅ SUPABASE_URL correto no `.env`?
2. ✅ SUPABASE_SERVICE_KEY válido?
3. ✅ Tabela `daily_metrics` existe?
4. ✅ RLS (Row Level Security) configurado?

---

## 📅 Manutenção

### Diária

- ✅ Verificar health: `.\scripts\health-check.ps1`
- ✅ Ver logs de erros
- ✅ Verificar se métricas foram coletadas

### Semanal

- ✅ Verificar espaço em disco (logs, cache)
- ✅ Review de dashboards Superset
- ✅ Backup do banco (PostgreSQL)

### Mensal

- ✅ Atualizar dependências: `pip list --outdated`
- ✅ Verificar validade do token Facebook (~60 dias)
- ✅ Review de segurança
- ✅ Limpar logs antigos

### A Cada 60 Dias

- ⚠️ **CRÍTICO:** Renovar Facebook Access Token
  1. Acessar Graph API Explorer
  2. Gerar novo token
  3. Converter para longa duração
  4. Atualizar `.env`
  5. Reiniciar containers

---

## 📊 Monitoramento

### Métricas Disponíveis (Prometheus)

- **Backend API:**
  - Request count
  - Request duration (P50, P95, P99)
  - Error rate
  - Active connections

- **PostgreSQL:**
  - Connections
  - Query duration
  - Cache hit rate

**Acesso:** http://localhost:9090

### Logs

**Localização:**
- Backend: `backend/logs/app.log`
- Docker: `docker-compose logs`

**Níveis:**
- INFO: Operações normais
- WARNING: Atenção necessária
- ERROR: Falhas que precisam correção
- CRITICAL: Sistema comprometido

---

## 🔑 Credenciais e Segurança

### Gerenciamento de .env

**NUNCA commitar `.env` no Git!**

**Rotacionar credenciais:**
```powershell
# Gerar novas keys
.\scripts\setup.ps1  # Exibe novas keys

# Atualizar .env
notepad .env

# Reiniciar serviços
docker-compose -f docker-compose.integrated.yml restart
```

### Backup de Credenciais

**Armazenar com segurança:**
- ✅ Password manager (1Password, Bitwarden)
- ✅ Vault (HashiCorp Vault)
- ❌ NUNCA em email ou documentos

---

## 📚 Recursos Úteis

### Documentação

- **Início Rápido:** `docs/development/QUICK-START.md`
- **Arquitetura:** `docs/architecture/ARCHITECTURE.md`
- **Integração:** `docs/operations/INTEGRATION-GUIDE.md`
- **PRDs:** `docs/product/`

### Scripts

- `scripts/setup.ps1` - Setup inicial
- `scripts/health-check.ps1` - Verificação saúde
- `scripts/validate-integration.py` - Validação completa
- `scripts/test-facebook.py` - Teste Facebook API

### Suporte

- **Issues:** https://github.com/Marcocardoso91/marketing-automation/issues
- **Docs:** https://github.com/Marcocardoso91/marketing-automation/tree/main/docs

---

## 🎯 Próximos Passos

**Após setup inicial:**
1. ✅ Configurar permissões Facebook
2. ✅ Testar coleta de métricas
3. ✅ Configurar dashboards Superset
4. ✅ Importar workflows N8N (opcional)
5. ✅ Configurar alertas Slack (opcional)

**Para produção:**
1. Configurar domínio (ex: api.macspark.dev)
2. Configurar HTTPS com Let's Encrypt
3. Configurar backups automáticos
4. Configurar monitoring/alerting
5. Configurar CI/CD para deploys

---

**Dúvidas?** Consulte `docs/INDEX.md` para navegação completa da documentação.

