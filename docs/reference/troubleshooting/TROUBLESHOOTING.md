# 🔧 Troubleshooting - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 🚨 Problemas Críticos

### Sistema Não Inicia

#### ❌ Docker Compose Falha
**Sintomas:** `docker-compose up` falha com erro

**Soluções:**
```powershell
# 1. Verificar Docker está rodando
docker --version
docker-compose --version

# 2. Limpar containers antigos
docker-compose down --volumes --remove-orphans
docker system prune -f

# 3. Reconstruir imagens
docker-compose build --no-cache
docker-compose up -d
```

#### ❌ Portas Ocupadas
**Sintomas:** `Port 8000 is already in use`

**Soluções:**
```powershell
# Verificar portas em uso
netstat -ano | findstr :8000
netstat -ano | findstr :8088
netstat -ano | findstr :9090

# Matar processo se necessário
taskkill /PID <PID_NUMBER> /F

# Ou usar portas alternativas no docker-compose.yml
```

#### ❌ Permissões Insuficientes
**Sintomas:** `Access denied` ou `Permission denied`

**Soluções:**
```powershell
# Executar PowerShell como Administrador
# Verificar permissões de pasta
icacls C:\Users\marco\Macspark\marketing-automation

# Dar permissões completas se necessário
icacls C:\Users\marco\Macspark\marketing-automation /grant Everyone:F /T
```

---

## 🔧 Problemas de Configuração

### ❌ Arquivo .env Incorreto
**Sintomas:** API retorna 500, logs mostram `KeyError`

**Soluções:**
```powershell
# 1. Verificar arquivo .env existe
Test-Path .env

# 2. Verificar variáveis obrigatórias
Get-Content .env | Select-String "FACEBOOK_ACCESS_TOKEN"
Get-Content .env | Select-String "SUPABASE_URL"

# 3. Recriar .env se necessário
Copy-Item env.template .env
notepad .env
```

**Variáveis Obrigatórias:**
```bash
# Facebook API
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key

# API
API_SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

### ❌ Credenciais Facebook Inválidas
**Sintomas:** `Facebook API Error: Invalid access token`

**Soluções:**
1. **Verificar token no Facebook Graph API Explorer:**
   - Acesse: https://developers.facebook.com/tools/explorer/
   - Teste: `GET /me` com seu token

2. **Renovar token se necessário:**
   - Facebook Business Manager → Apps → Seu App → Tokens
   - Gerar novo token com permissões: `ads_read`, `ads_management`

3. **Verificar permissões:**
   ```bash
   # Testar token via curl
   curl -X GET "https://graph.facebook.com/v18.0/me?access_token=YOUR_TOKEN"
   ```

### ❌ Conexão Supabase Falha
**Sintomas:** `Connection refused` ou `Invalid URL`

**Soluções:**
```powershell
# 1. Verificar URL Supabase
$env:SUPABASE_URL
# Deve ser: https://xxxxx.supabase.co

# 2. Testar conexão
curl -X GET "$env:SUPABASE_URL/rest/v1/" -H "apikey: $env:SUPABASE_KEY"

# 3. Verificar chave API
# Supabase Dashboard → Settings → API → anon key
```

---

## 🚀 Problemas de Runtime

### ❌ API Não Responde (500/502/503)
**Sintomas:** `http://localhost:8000` retorna erro

**Diagnóstico:**
```powershell
# 1. Verificar logs do container
docker-compose logs api

# 2. Verificar saúde do serviço
.\scripts\health-check.ps1

# 3. Testar endpoint específico
curl -X GET "http://localhost:8000/health"
```

**Soluções Comuns:**
```powershell
# 1. Reiniciar API
docker-compose restart api

# 2. Verificar dependências
docker-compose exec api pip list

# 3. Reconstruir container
docker-compose down api
docker-compose up -d api
```

### ❌ Coleta de Métricas Falha
**Sintomas:** `/api/v1/metrics/export` retorna erro

**Diagnóstico:**
```powershell
# 1. Verificar logs específicos
docker-compose logs api | Select-String "Facebook"
docker-compose logs api | Select-String "Error"

# 2. Testar Facebook API diretamente
curl -X GET "https://graph.facebook.com/v18.0/me/adaccounts?access_token=YOUR_TOKEN"
```

**Soluções:**
1. **Verificar token Facebook válido**
2. **Verificar permissões de conta**
3. **Verificar rate limits (200 calls/hora)**
4. **Verificar datas válidas (não futuras)**

### ❌ Superset Não Carrega
**Sintomas:** `http://localhost:8088` não abre

**Soluções:**
```powershell
# 1. Verificar container Superset
docker-compose ps superset

# 2. Verificar logs
docker-compose logs superset

# 3. Reiniciar Superset
docker-compose restart superset

# 4. Aguardar inicialização (pode levar 2-3 minutos)
```

---

## 🔌 Problemas de Integração

### ❌ N8N Workflows Falham
**Sintomas:** Workflows não executam ou falham

**Diagnóstico:**
```powershell
# 1. Verificar N8N está rodando
docker-compose ps n8n

# 2. Acessar interface N8N
# http://localhost:5678

# 3. Verificar credenciais nos workflows
```

**Soluções:**
1. **Verificar credenciais configuradas**
2. **Testar conexões individualmente**
3. **Verificar rate limits das APIs**
4. **Reconfigurar workflows se necessário**

### ❌ Notion Integration Falha
**Sintomas:** Relatórios não são salvos no Notion

**Diagnóstico:**
```powershell
# 1. Verificar token Notion
$env:NOTION_API_KEY

# 2. Testar API Notion
curl -X GET "https://api.notion.com/v1/users/me" -H "Authorization: Bearer $env:NOTION_API_KEY"
```

**Soluções:**
1. **Verificar token Notion válido**
2. **Verificar database ID correto**
3. **Verificar permissões de escrita**
4. **Verificar estrutura do database**

---

## 📊 Problemas de Analytics

### ❌ Superset Dashboards Não Carregam
**Sintomas:** Dashboards mostram "No data" ou erro

**Soluções:**
```powershell
# 1. Verificar conexão Supabase
# Superset → Data → Databases → Supabase

# 2. Testar query SQL
# Superset → SQL Lab → Test query

# 3. Verificar dados no Supabase
# Supabase Dashboard → Table Editor
```

### ❌ Dados Não Aparecem
**Sintomas:** Métricas não são coletadas ou não aparecem

**Diagnóstico:**
```powershell
# 1. Verificar coleta funcionando
curl -X GET "http://localhost:8000/api/v1/metrics/export?date_from=2025-10-20&date_until=2025-10-23" -H "X-API-Key: your_key"

# 2. Verificar dados no Supabase
# Supabase Dashboard → Table Editor → campaigns
```

---

## 🐛 Debugging e Logs

### 📋 Checklist de Diagnóstico

```powershell
# 1. Verificar saúde geral
.\scripts\health-check.ps1

# 2. Verificar logs de todos os serviços
docker-compose logs --tail=50

# 3. Verificar recursos do sistema
docker stats

# 4. Verificar conectividade
Test-NetConnection localhost -Port 8000
Test-NetConnection localhost -Port 8088
Test-NetConnection localhost -Port 9090
```

### 📝 Logs Importantes

**API Logs:**
```powershell
docker-compose logs api | Select-String "ERROR"
docker-compose logs api | Select-String "Facebook"
docker-compose logs api | Select-String "Supabase"
```

**Superset Logs:**
```powershell
docker-compose logs superset | Select-String "ERROR"
docker-compose logs superset | Select-String "Connection"
```

**N8N Logs:**
```powershell
docker-compose logs n8n | Select-String "ERROR"
docker-compose logs n8n | Select-String "Workflow"
```

---

## 🆘 Problemas Específicos por Serviço

### Facebook API
- **Rate Limit Exceeded:** Aguardar 1 hora ou usar token diferente
- **Invalid Token:** Renovar no Facebook Business Manager
- **Permission Denied:** Verificar permissões da conta
- **Account Suspended:** Contatar suporte Facebook

### Supabase
- **Connection Timeout:** Verificar URL e chave
- **Row Level Security:** Verificar políticas de segurança
- **Quota Exceeded:** Verificar plano Supabase

### Docker
- **Out of Memory:** Aumentar memória Docker Desktop
- **Port Conflicts:** Verificar portas disponíveis
- **Volume Issues:** Verificar permissões de pasta

---

## 📞 Suporte e Recursos

### 🔗 Links Úteis
- **Facebook Graph API:** https://developers.facebook.com/docs/graph-api
- **Supabase Docs:** https://supabase.com/docs
- **Apache Superset:** https://superset.apache.org/docs
- **N8N Docs:** https://docs.n8n.io

### 📧 Contato
- **Issues GitHub:** [Criar issue](https://github.com/your-repo/issues)
- **Documentação:** [docs/INDEX.md](../../INDEX.md)
- **Logs Completos:** `docker-compose logs > logs.txt`

---

## ✅ Resolução Rápida

### Problema Mais Comum: Sistema Não Inicia
```powershell
# Solução em 3 passos:
1. docker-compose down --volumes
2. Copy-Item env.template .env
3. docker-compose up -d
```

### Problema Mais Comum: API 500 Error
```powershell
# Solução em 2 passos:
1. Verificar .env tem todas as variáveis
2. docker-compose restart api
```

### Problema Mais Comum: Superset Não Carrega
```powershell
# Solução em 1 passo:
1. Aguardar 3-5 minutos (inicialização lenta)
```

---

**💡 Dica:** Se nada funcionar, execute `.\scripts\setup.ps1` para reconfigurar tudo do zero.
