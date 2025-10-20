# 🔒 Guia de Segurança - API Keys e Credenciais

**Data:** 20 de Outubro, 2025
**Versão:** 1.0.0
**Status:** ✅ Implementado

---

## 🎯 Objetivo

Este guia ensina como proteger suas chaves de API (OpenAI, Slack, YouTube, TikTok, etc.) contra roubo e uso indevido.

---

## ✅ Proteções Já Implementadas

### 1. `.gitignore` Configurado

Todos os arquivos `.env` estão **automaticamente ignorados** pelo Git:

```gitignore
.env
.env.local
.env.*.local
.env.mcp
```

**Status:** ✅ Verificado - Nenhum `.env` foi commitado no histórico

### 2. Arquivos de Template

Usamos arquivos `.env.example` que **não contêm chaves reais**:
- `env.template` (raiz)
- `analytics/scripts/env.example.txt`

---

## 🛡️ Níveis de Segurança

### Nível 1: Básico ✅ (Implementado)

- ✅ `.env` no `.gitignore`
- ✅ Chaves não commitadas
- ✅ Templates documentados

### Nível 2: Recomendado 🔒 (Implementar)

- 🔒 Rotação periódica de chaves
- 🔒 Permissões mínimas (read-only quando possível)
- 🔒 Monitoramento de uso
- 🔒 Rate limits configurados

### Nível 3: Avançado 🚀 (Opcional)

- 🚀 Vault de secrets (HashiCorp Vault, AWS Secrets Manager)
- 🚀 Variáveis de ambiente no CI/CD
- 🚀 Criptografia em repouso
- 🚀 Autenticação multi-fator

---

## 🔐 Configuração Segura por Serviço

### 1. OpenAI (Insights com IA)

#### ⚠️ Riscos
- **Custo:** Uso indevido pode gerar custos altos
- **Dados:** Prompts podem conter dados sensíveis

#### ✅ Boas Práticas

**a) Criar chave com permissões limitadas:**
1. Acesse: https://platform.openai.com/api-keys
2. Clique em **"Create new secret key"**
3. **Nome:** `Marketing Automation - Insights (Read Only)`
4. **Permissões:**
   - ✅ **Model capabilities:** `gpt-4o-mini` apenas
   - ❌ **Fine-tuning:** Desabilitado
   - ❌ **File upload:** Desabilitado
5. **Limite de gasto mensal:** $10 (Configure em "Usage limits")

**b) Configurar no `.env`:**
```bash
# OpenAI (Insights IA)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini  # Modelo mais barato
OPENAI_MAX_TOKENS=500     # Limita tamanho da resposta
```

**c) Monitorar uso:**
- Dashboard: https://platform.openai.com/usage
- Configure alerta de gasto em **Settings** → **Billing**

#### 🔒 Segurança Extra
```python
# No código, adicionar timeout e retry limit
openai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=10.0,  # Timeout de 10s
    max_retries=2   # Máximo 2 tentativas
)
```

---

### 2. Slack (Notificações)

#### ⚠️ Riscos
- **Spam:** Webhook pode ser usado para spam
- **Dados vazados:** Mensagens com dados sensíveis

#### ✅ Boas Práticas

**a) Criar Incoming Webhook (Mais Seguro):**
1. Acesse: https://api.slack.com/apps
2. **"Create New App"** → **"From scratch"**
3. Nome: `Marketing Metrics Bot`
4. Workspace: Escolha seu workspace
5. **Features** → **Incoming Webhooks** → Ative
6. **"Add New Webhook to Workspace"**
7. Escolha um canal **privado** (ex: `#marketing-metrics-private`)
8. Copie o Webhook URL

**b) Configurar no `.env`:**
```bash
# Slack (Notificações)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00/B00/XXXX
```

**c) Limitar mensagens:**
```python
# Adicionar rate limit no código
from datetime import datetime, timedelta

last_notification = None
NOTIFICATION_INTERVAL = timedelta(hours=24)  # Max 1x/dia

def send_slack_notification(message):
    global last_notification

    if last_notification and datetime.now() - last_notification < NOTIFICATION_INTERVAL:
        print("⏳ Aguardando intervalo entre notificações")
        return False

    # Enviar notificação...
    last_notification = datetime.now()
```

#### 🔒 Segurança Extra
- Use canal **privado** (não #general)
- Não envie dados sensíveis (senhas, tokens)
- Configure alertas apenas para eventos importantes

---

### 3. YouTube Data API v3

#### ⚠️ Riscos
- **Quota:** 10.000 unidades/dia (gratuito)
- **Dados públicos:** Menos risco, mas quota pode acabar

#### ✅ Boas Práticas

**a) Criar API Key (Read-Only):**
1. Acesse: https://console.cloud.google.com/apis/dashboard
2. **"Create Project"** → Nome: `Marketing Automation`
3. **"Enable APIs"** → Buscar **"YouTube Data API v3"** → Enable
4. **Credentials** → **"Create Credentials"** → **API Key**
5. **Restrict Key:**
   - **Application restrictions:** None (ou IP do servidor)
   - **API restrictions:** YouTube Data API v3 apenas
6. Copie a API Key

**b) Configurar no `.env`:**
```bash
# YouTube Data API v3
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxx  # ID do seu canal
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx
```

**c) Encontrar seu Channel ID:**
- Método 1: https://www.youtube.com/@SEU_USUARIO → Ver código-fonte → buscar "channelId"
- Método 2: https://commentpicker.com/youtube-channel-id.php

#### 🔒 Segurança Extra
```python
# Cachear resultados para economizar quota
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1)
def get_youtube_metrics_cached():
    # Buscar apenas 1x por dia
    return get_youtube_metrics()
```

---

### 4. TikTok API (NOVO)

#### ⚠️ Riscos
- **Aprovação:** API requer aprovação do TikTok
- **Quota:** Limitada (varia por conta)

#### ✅ Boas Práticas

**a) Solicitar acesso à API:**
1. Acesse: https://developers.tiktok.com/
2. **"Get Started"** → **Register**
3. Criar app: **"TikTok for Business"** → **"Marketing API"**
4. Preencher formulário (pode levar 1-2 dias para aprovação)

**b) Após aprovação, gerar Access Token:**
1. Dashboard: https://ads.tiktok.com/marketing_api/apps
2. **"Create Access Token"**
3. **Permissões:**
   - ✅ `user.info.basic` (informações básicas)
   - ✅ `video.list` (listar vídeos)
   - ✅ `video.data` (métricas de vídeo)
   - ❌ **NÃO** dar permissões de escrita

**c) Configurar no `.env`:**
```bash
# TikTok API (Marketing API)
TIKTOK_ACCESS_TOKEN=act.xxxxxxxxxxxxxxxx
TIKTOK_APP_ID=123456789
TIKTOK_APP_SECRET=xxxxxxxxxxxxxxxx
TIKTOK_ADVERTISER_ID=123456789  # ID da conta de anúncios
```

**Nota:** Se você **não usa TikTok Ads**, use a **Display API** (mais limitada):
```bash
# TikTok Display API (sem anúncios)
TIKTOK_CLIENT_KEY=awxxxxxxxxxx
TIKTOK_CLIENT_SECRET=xxxxxxxxxxxxxxxx
TIKTOK_USERNAME=seu_usuario_tiktok
```

---

## 🚨 O Que Fazer se uma Chave Vazar

### 1. **REVOGUE IMEDIATAMENTE**

**OpenAI:**
1. https://platform.openai.com/api-keys
2. Encontre a chave → **"Revoke"**
3. Crie nova chave

**Slack:**
1. https://api.slack.com/apps
2. Seu app → **"Incoming Webhooks"**
3. Delete o webhook antigo
4. Crie novo

**YouTube/Google:**
1. https://console.cloud.google.com/apis/credentials
2. Encontre a chave → **"Delete"**
3. Crie nova

**TikTok:**
1. https://ads.tiktok.com/marketing_api/apps
2. **"Revoke Access Token"**
3. Gere novo

### 2. **VERIFIQUE O HISTÓRICO DO GIT**

```bash
# Verificar se .env foi commitado
git log --all --full-history --source -- "*.env"

# Se encontrou commits com .env, REESCREVA O HISTÓRICO:
# ⚠️ CUIDADO: Isso reescreve todo o histórico!
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch **/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (se necessário)
git push origin --force --all
```

### 3. **MONITORE O USO**

- **OpenAI:** https://platform.openai.com/usage (verificar cobranças anormais)
- **YouTube:** https://console.cloud.google.com/apis/dashboard (verificar quota)
- **Slack:** Verificar mensagens no canal
- **TikTok:** Dashboard de uso da API

---

## 📋 Checklist de Segurança

Antes de adicionar qualquer chave:

- [ ] ✅ Verificar que `.env` está no `.gitignore`
- [ ] ✅ Nunca commitar `.env` no Git
- [ ] ✅ Usar permissões mínimas (read-only quando possível)
- [ ] ✅ Configurar limites de gasto/quota
- [ ] ✅ Usar canais privados (Slack)
- [ ] ✅ Monitorar uso regularmente
- [ ] ✅ Documentar onde cada chave é usada
- [ ] ✅ Rotacionar chaves a cada 90 dias

---

## 🎓 Boas Práticas Gerais

### 1. Nunca Hardcode Chaves

❌ **ERRADO:**
```python
OPENAI_API_KEY = "sk-proj-abc123..."  # NUNCA FAÇA ISSO!
```

✅ **CORRETO:**
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 2. Valide Antes de Usar

```python
required_keys = ["OPENAI_API_KEY", "SLACK_WEBHOOK_URL"]
missing = [key for key in required_keys if not os.getenv(key)]

if missing:
    raise ValueError(f"Chaves faltando: {', '.join(missing)}")
```

### 3. Use Diferentes Chaves por Ambiente

```bash
# Desenvolvimento (.env.local)
OPENAI_API_KEY=sk-proj-dev-xxx

# Produção (.env.production)
OPENAI_API_KEY=sk-proj-prod-yyy
```

### 4. Rotate Regularmente

Configure lembretes para rotacionar chaves:
- **OpenAI:** A cada 90 dias
- **Slack Webhook:** A cada 180 dias
- **YouTube API:** Apenas se houver suspeita
- **TikTok:** A cada 90 dias

---

## 🔗 Links Úteis

- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **OpenAI Usage:** https://platform.openai.com/usage
- **Slack Webhooks:** https://api.slack.com/messaging/webhooks
- **Google Cloud Console:** https://console.cloud.google.com/
- **TikTok for Developers:** https://developers.tiktok.com/
- **1Password (gerenciar senhas):** https://1password.com/
- **Bitwarden (alternativa gratuita):** https://bitwarden.com/

---

## ❓ FAQ

**P: Posso compartilhar meu `.env` com a equipe?**
R: NÃO! Use um gerenciador de senhas (1Password, Bitwarden) ou variáveis de ambiente do servidor.

**P: O que fazer se eu acidentalmente commitar um `.env`?**
R: Siga a seção "O Que Fazer se uma Chave Vazar" imediatamente.

**P: Qual a diferença entre `.env` e `env.template`?**
R: `env.template` é um exemplo (pode commitar), `.env` tem chaves reais (NUNCA commitar).

**P: Preciso de todas essas APIs?**
R: Não! Comece apenas com as que você vai usar. OpenAI e Slack são opcionais.

---

**Última atualização:** 20 de Outubro, 2025
