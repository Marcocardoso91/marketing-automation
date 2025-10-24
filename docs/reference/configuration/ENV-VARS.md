# ⚙️ Variáveis de Ambiente - Marketing Automation Platform

**Versão:** 1.0.0  
**Última atualização:** 23 de Outubro, 2025

---

## 📋 Visão Geral

Este documento lista todas as variáveis de ambiente necessárias para o funcionamento completo do Marketing Automation Platform, organizadas por categoria e prioridade.

---

## 🔴 **OBRIGATÓRIAS** (Sistema não funciona sem elas)

### Facebook API
```bash
# Identificação da aplicação Facebook
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret

# Token de acesso para coleta de dados
FACEBOOK_ACCESS_TOKEN=EAA_your_facebook_token_here

# ID da conta de anúncios
FACEBOOK_AD_ACCOUNT_ID=act_123456789
```

### Database & Cache
```bash
# PostgreSQL - Banco principal
POSTGRES_USER=fbads_admin
POSTGRES_PASSWORD=REPLACE_ME_STRONG_PASSWORD

# Redis - Cache e sessões
REDIS_URL=redis://localhost:6379/0
```

### Segurança
```bash
# Chave secreta da aplicação (mínimo 64 caracteres)
SECRET_KEY=REPLACE_ME_MIN_64_RANDOM_CHARS

# Chave para API de analytics
ANALYTICS_API_KEY=REPLACE_ME_MIN_64_RANDOM_CHARS
```

---

## 🟡 **IMPORTANTES** (Funcionalidades limitadas sem elas)

### Supabase (Data Warehouse)
```bash
# URL do projeto Supabase
SUPABASE_URL=https://your-project.supabase.co

# Chave anônima (pública)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Chave de serviço (privada)
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### N8N (Automação)
```bash
# URL base do N8N
N8N_WEBHOOK_URL=https://fluxos.macspark.dev/webhook
N8N_API_URL=https://fluxos.macspark.dev/api/v1

# Chave de API do N8N
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Autenticação básica
N8N_BASIC_AUTH_USER=n8n_admin
N8N_BASIC_AUTH_PASSWORD=REPLACE_ME_STRONG_PASSWORD
```

### Superset (Business Intelligence)
```bash
# Chave secreta do Superset
SUPERSET_SECRET_KEY=your_superset_secret_key_here

# Senha do administrador
SUPERSET_ADMIN_PASSWORD=admin_change_me
```

---

## 🟢 **OPCIONAIS** (Funcionalidades extras)

### Notion Integration
```bash
# Token da API Notion
NOTION_API_TOKEN=secret_your_notion_token

# ID do database Notion
NOTION_DATABASE_ID=your_database_id
```

### Slack Integration
```bash
# Webhook URL do Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Google APIs (Analytics)
```bash
# Credenciais Google para GA4
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

### OpenAI (IA)
```bash
# Chave da API OpenAI
OPENAI_API_KEY=sk-your_openai_key
```

### Grafana (Monitoramento)
```bash
# Credenciais do Grafana
GRAFANA_ADMIN_USER=grafana_admin
GRAFANA_ADMIN_PASSWORD=REPLACE_ME_STRONG_PASSWORD
```

---

## 🔧 **CONFIGURAÇÃO** (Ambiente e URLs)

### Ambiente
```bash
# Ambiente de execução
ENVIRONMENT=production  # ou development, staging

# Modo debug
DEBUG=false  # ou true para desenvolvimento

# URL da API Agent
AGENT_API_URL=http://agent-api:8000
```

### Segurança Avançada
```bash
# Origens permitidas (CORS)
ALLOWED_ORIGINS=https://fbads.macspark.dev,https://api.fbads.macspark.dev

# Hosts confiáveis
TRUSTED_HOSTS=fbads.macspark.dev,api.fbads.macspark.dev,*.macspark.dev
```

---

## 📝 **EXEMPLO COMPLETO** (.env)

```bash
# ========================================
# FACEBOOK API (OBRIGATÓRIO)
# ========================================
FACEBOOK_APP_ID=1234567890123456
FACEBOOK_APP_SECRET=abcdef1234567890abcdef1234567890
FACEBOOK_ACCESS_TOKEN=EAA_your_facebook_token_here
FACEBOOK_AD_ACCOUNT_ID=act_123456789

# ========================================
# DATABASE & CACHE (OBRIGATÓRIO)
# ========================================
POSTGRES_USER=fbads_admin
POSTGRES_PASSWORD=MySecurePassword123!
REDIS_URL=redis://localhost:6379/0

# ========================================
# SEGURANÇA (OBRIGATÓRIO)
# ========================================
SECRET_KEY=MySecretKey123456789012345678901234567890123456789012345678901234567890
ANALYTICS_API_KEY=MyAnalyticsKey123456789012345678901234567890123456789012345678901234567890

# ========================================
# SUPABASE (IMPORTANTE)
# ========================================
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5ODc2MDAwMCwiZXhwIjoyMDE0MzM2MDAwfQ.example
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjk4NzYwMDAwLCJleHAiOjIwMTQzMzYwMDB9.example

# ========================================
# N8N (IMPORTANTE)
# ========================================
N8N_WEBHOOK_URL=https://fluxos.macspark.dev/webhook
N8N_API_URL=https://fluxos.macspark.dev/api/v1
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example
N8N_BASIC_AUTH_USER=n8n_admin
N8N_BASIC_AUTH_PASSWORD=MyN8NPassword123!

# ========================================
# SUPERSET (IMPORTANTE)
# ========================================
SUPERSET_SECRET_KEY=MySupersetSecretKey123456789012345678901234567890
SUPERSET_ADMIN_PASSWORD=MySupersetPassword123!

# ========================================
# INTEGRAÇÕES (OPCIONAL)
# ========================================
NOTION_API_TOKEN=secret_abcdefghijklmnopqrstuvwxyz1234567890
NOTION_DATABASE_ID=abcdefgh-1234-5678-9012-abcdefghijkl
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz1234567890

# ========================================
# GOOGLE APIs (OPCIONAL)
# ========================================
GOOGLE_CLIENT_ID=123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz123456

# ========================================
# GRAFANA (OPCIONAL)
# ========================================
GRAFANA_ADMIN_USER=grafana_admin
GRAFANA_ADMIN_PASSWORD=MyGrafanaPassword123!

# ========================================
# CONFIGURAÇÃO (OPCIONAL)
# ========================================
ENVIRONMENT=production
DEBUG=false
AGENT_API_URL=http://agent-api:8000
ALLOWED_ORIGINS=https://fbads.macspark.dev,https://api.fbads.macspark.dev
TRUSTED_HOSTS=fbads.macspark.dev,api.fbads.macspark.dev,*.macspark.dev
```

---

## 🔐 **COMO OBTER CREDENCIAIS**

### Facebook API
1. **Acessar:** https://developers.facebook.com/apps
2. **Criar App** → Tipo: "Empresa"
3. **Adicionar Marketing API**
4. **Gerar Access Token** com permissões:
   - `ads_read`
   - `ads_management`
   - `business_management`

### Supabase
1. **Acessar:** https://supabase.com
2. **Criar projeto**
3. **Settings → API**
4. **Copiar:**
   - Project URL → `SUPABASE_URL`
   - anon key → `SUPABASE_ANON_KEY`
   - service_role key → `SUPABASE_SERVICE_KEY`

### Notion
1. **Acessar:** https://www.notion.so/my-integrations
2. **New integration**
3. **Copiar Integration Token** → `NOTION_API_TOKEN`
4. **Compartilhar database** com integration
5. **Copiar Database ID** da URL

### N8N
1. **Acessar:** https://fluxos.macspark.dev
2. **Settings → API Keys**
3. **Generate new key** → `N8N_API_KEY`

### OpenAI
1. **Acessar:** https://platform.openai.com/api-keys
2. **Create new secret key** → `OPENAI_API_KEY`

---

## 🔄 **ROTAÇÃO DE SECRETS**

### Rotação Automática
```bash
# Script para rotar secrets (exemplo)
#!/bin/bash

# Gerar nova SECRET_KEY
NEW_SECRET=$(openssl rand -base64 64)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$NEW_SECRET/" .env

# Gerar nova ANALYTICS_API_KEY
NEW_ANALYTICS=$(openssl rand -base64 64)
sed -i "s/ANALYTICS_API_KEY=.*/ANALYTICS_API_KEY=$NEW_ANALYTICS/" .env

echo "✅ Secrets rotacionados com sucesso"
```

### Rotação Manual
1. **Gerar novos secrets:**
   ```bash
   # SECRET_KEY (64 caracteres)
   openssl rand -base64 64
   
   # ANALYTICS_API_KEY (64 caracteres)
   openssl rand -base64 64
   ```

2. **Atualizar .env**
3. **Reiniciar serviços:**
   ```bash
   docker-compose restart api
   ```

---

## 🛡️ **BOAS PRÁTICAS DE SEGURANÇA**

### 1. Proteção do Arquivo .env
```bash
# Definir permissões restritivas
chmod 600 .env

# Não commitar no Git
echo ".env" >> .gitignore
```

### 2. Validação de Secrets
```bash
# Verificar se secrets são seguros
if [ ${#SECRET_KEY} -lt 64 ]; then
  echo "❌ SECRET_KEY muito curta (mínimo 64 caracteres)"
fi

if [ ${#ANALYTICS_API_KEY} -lt 64 ]; then
  echo "❌ ANALYTICS_API_KEY muito curta (mínimo 64 caracteres)"
fi
```

### 3. Monitoramento de Acesso
```bash
# Log de acessos às variáveis sensíveis
grep -r "SECRET_KEY\|ANALYTICS_API_KEY" /var/log/
```

### 4. Backup Seguro
```bash
# Backup criptografado do .env
gpg --symmetric --cipher-algo AES256 .env
```

---

## 🚨 **TROUBLESHOOTING**

### Problemas Comuns

#### ❌ Variável Não Encontrada
**Sintomas:** `KeyError: 'VARIABLE_NAME'`

**Soluções:**
1. **Verificar** se variável existe no .env
2. **Verificar** se não há espaços extras
3. **Verificar** se não há caracteres especiais
4. **Reiniciar** aplicação após mudanças

#### ❌ Credencial Inválida
**Sintomas:** `401 Unauthorized` ou `Invalid token`

**Soluções:**
1. **Verificar** formato da credencial
2. **Testar** credencial manualmente
3. **Renovar** credencial se expirada
4. **Verificar** permissões

#### ❌ Database Connection Failed
**Sintomas:** `Connection refused` ou `Database not found`

**Soluções:**
1. **Verificar** URL do database
2. **Verificar** credenciais
3. **Verificar** se database existe
4. **Testar** conexão manualmente

### Validação de Configuração

```bash
# Script de validação
#!/bin/bash

echo "🔍 Validando configuração..."

# Verificar arquivo .env existe
if [ ! -f .env ]; then
  echo "❌ Arquivo .env não encontrado"
  exit 1
fi

# Verificar variáveis obrigatórias
required_vars=(
  "FACEBOOK_APP_ID"
  "FACEBOOK_ACCESS_TOKEN"
  "SECRET_KEY"
  "ANALYTICS_API_KEY"
)

for var in "${required_vars[@]}"; do
  if ! grep -q "^${var}=" .env; then
    echo "❌ Variável obrigatória $var não encontrada"
    exit 1
  fi
done

echo "✅ Configuração válida"
```

---

## 📊 **MONITORAMENTO**

### Métricas Importantes
- **Taxa de sucesso** das conexões
- **Tempo de resposta** das APIs
- **Erros de autenticação**
- **Rate limits** excedidos

### Alertas Recomendados
1. **Credencial expira** em 7 dias
2. **Rate limit** excedido
3. **Conexão falha** consecutivamente
4. **Secret rotacionado** com sucesso

---

## 🔗 **RECURSOS ADICIONAIS**

### Documentação
- **Troubleshooting:** [docs/reference/troubleshooting/TROUBLESHOOTING.md](../troubleshooting/TROUBLESHOOTING.md)
- **API Reference:** [docs/api/agent-api/API-REFERENCE.md](../../api/agent-api/API-REFERENCE.md)
- **Security Guide:** [docs/operations/SECURITY-API-KEYS.md](../../operations/SECURITY-API-KEYS.md)

### Scripts Úteis
- **Validação:** `scripts/validate-env.sh`
- **Rotação:** `scripts/rotate-secrets.sh`
- **Backup:** `scripts/backup-env.sh`

### Suporte
- **GitHub Issues:** [Criar issue](https://github.com/your-repo/issues)
- **Documentação:** [docs/INDEX.md](../../INDEX.md)

---

## ✅ **CHECKLIST DE CONFIGURAÇÃO**

### Configuração Básica
- [ ] ✅ Arquivo .env criado
- [ ] ✅ Variáveis obrigatórias configuradas
- [ ] ✅ Credenciais Facebook válidas
- [ ] ✅ Database PostgreSQL funcionando
- [ ] ✅ Redis funcionando
- [ ] ✅ Secrets seguros (64+ caracteres)

### Configuração Avançada
- [ ] ✅ Supabase configurado
- [ ] ✅ N8N integrado
- [ ] ✅ Superset funcionando
- [ ] ✅ Integrações opcionais
- [ ] ✅ Monitoramento ativo
- [ ] ✅ Backup configurado

---

**💡 Dica:** Use `env.template` como base e substitua apenas os valores necessários!
