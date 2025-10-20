# 🚀 Setup Seguro - APIs (OpenAI, Slack, YouTube, TikTok)

**Tempo total:** ~20-30 minutos
**Última atualização:** 20 de Outubro, 2025

---

## 🎯 Visão Geral

Este guia ensina como configurar de forma **100% segura**:
- ✅ **OpenAI** (Insights com IA)
- ✅ **Slack** (Notificações)
- ✅ **YouTube** (Métricas de vídeos)
- ✅ **TikTok** (Métricas de vídeos)

**Todos são OPCIONAIS** - Configure apenas o que você vai usar!

---

## 🔒 Garantias de Segurança

Antes de começar, saiba que:

1. ✅ **Arquivos `.env` estão no `.gitignore`** → Nunca vão para o Git
2. ✅ **Nenhum arquivo `.env` foi commitado** → Histórico limpo
3. ✅ **Usamos permissões mínimas** → Read-only sempre que possível
4. ✅ **Configuramos limites de gasto** → Proteção contra uso excessivo
5. ✅ **Canais privados no Slack** → Sem exposição pública

---

## 1. OpenAI (Insights com IA) 🤖

### ⏱️ Tempo: 5 minutos
### 💰 Custo: ~$2-5/mês (1 insight/dia)

### Passo a Passo

**1. Criar conta OpenAI:**
- Acesse: https://platform.openai.com/signup
- Faça login com Google/Email
- **Adicione método de pagamento** (requer cartão)

**2. Configurar limite de gasto (IMPORTANTE!):**
- Vá em: https://platform.openai.com/settings/organization/limits
- **"Set a monthly budget"**: `$10` (suficiente para ~300 insights/mês)
- **"Email notifications"**: Marque para receber alertas

**3. Criar API Key:**
- Vá em: https://platform.openai.com/api-keys
- **"Create new secret key"**
- **Nome**: `Marketing Automation - Insights`
- **Permissões**:
  - ✅ Model capabilities: `gpt-4o-mini` apenas
  - ❌ All other permissions: Desabilitado
- **Copie a chave** (ela só aparece 1x!)

**4. Adicionar no `.env`:**
```bash
cd analytics/scripts
nano .env  # ou use seu editor favorito
```

Descomente e cole a chave:
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxx  # Sua chave aqui
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=500
```

**5. Testar:**
```bash
python -c "from openai import OpenAI; client = OpenAI(); print('✅ OpenAI configurado!')"
```

### 🛡️ Segurança Extra

- **Rotacione a chave a cada 90 dias**
- **Monitore uso**: https://platform.openai.com/usage
- **Se vazar**: Revogue imediatamente em https://platform.openai.com/api-keys

---

## 2. Slack (Notificações) 📢

### ⏱️ Tempo: 5 minutos
### 💰 Custo: Gratuito

### Passo a Passo

**1. Criar App no Slack:**
- Acesse: https://api.slack.com/apps
- **"Create New App"** → **"From scratch"**
- **App Name**: `Marketing Metrics Bot`
- **Workspace**: Escolha seu workspace

**2. Ativar Incoming Webhooks:**
- No menu lateral: **"Incoming Webhooks"**
- **"Activate Incoming Webhooks"**: Toggle ON
- **"Add New Webhook to Workspace"**

**3. Escolher Canal (IMPORTANTE!):**
- ⚠️ **NÃO** escolha `#general` ou canais públicos
- ✅ Escolha um canal **PRIVADO**: `#marketing-metrics-private`
- Se não tiver, crie um canal privado antes

**4. Copiar Webhook URL:**
- Após escolher o canal, copie o **Webhook URL**
- Será algo como: `https://hooks.slack.com/services/...` (cole no .env)

**5. Adicionar no `.env`:**
```bash
SLACK_WEBHOOK_URL=cole_seu_webhook_url_aqui
```

**6. Testar:**
```bash
python analytics/scripts/test-slack-webhook.py
```

Você deve receber uma mensagem de teste no canal!

### 🛡️ Segurança Extra

- ✅ Use canal **privado**
- ✅ Nunca envie dados sensíveis (senhas, tokens)
- ✅ Configure rate limit (max 1 notificação/hora)
- **Se vazar**: Delete o webhook e crie novo

---

## 3. YouTube (Métricas de Vídeos) 📺

### ⏱️ Tempo: 7 minutos
### 💰 Custo: Gratuito (quota: 10.000 unidades/dia)

### Passo a Passo

**1. Criar Projeto no Google Cloud:**
- Acesse: https://console.cloud.google.com/
- **"Create Project"**
- **Nome**: `Marketing Automation`
- **Organization**: Deixe em branco (ou escolha sua org)

**2. Ativar YouTube Data API v3:**
- Vá em: **"APIs & Services"** → **"Library"**
- Busque: `YouTube Data API v3`
- Clique em **"Enable"**

**3. Criar API Key:**
- Vá em: **"APIs & Services"** → **"Credentials"**
- **"Create Credentials"** → **"API Key"**
- Copie a API Key

**4. Restringir API Key (IMPORTANTE!):**
- Clique no ícone de lápis ao lado da key
- **"Application restrictions"**:
  - Se usar em servidor fixo: **"IP addresses"** → Adicione IP do servidor
  - Se usar localmente: **"None"** (menos seguro, mas OK para testes)
- **"API restrictions"**: **"Restrict key"**
  - Selecione: ✅ **"YouTube Data API v3"** apenas
- **"Save"**

**5. Encontrar seu Channel ID:**
- **Método 1**: https://commentpicker.com/youtube-channel-id.php
  - Cole o link do seu canal
  - Copie o Channel ID (formato: `UCxxxxxxxxxxxx`)

- **Método 2**: Manualmente
  - Acesse seu canal no YouTube
  - Veja código-fonte da página (Ctrl+U)
  - Busque por `"channelId"`

**6. Adicionar no `.env`:**
```bash
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxx  # Seu Channel ID
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx  # Sua API Key
```

**7. Testar:**
```bash
cd analytics/scripts
python -c "from collectors.youtube_collector import get_youtube_metrics; print(get_youtube_metrics())"
```

### 🛡️ Segurança Extra

- ✅ Restrinja a key apenas para YouTube Data API v3
- ✅ Monitore quota: https://console.cloud.google.com/apis/dashboard
- ✅ 10.000 unidades/dia é suficiente para ~30 requisições/dia
- **Se vazar**: Delete a key e crie nova

---

## 4. TikTok (Métricas de Vídeos) 🎵

### ⏱️ Tempo: 10-15 minutos (+ 1-2 dias para aprovação)
### 💰 Custo: Gratuito

### Opção 1: TikTok Marketing API (para quem usa TikTok Ads)

**1. Acessar TikTok for Business:**
- Acesse: https://ads.tiktok.com/
- Faça login com sua conta TikTok

**2. Ir para Developer Portal:**
- https://ads.tiktok.com/marketing_api/apps
- **"Create App"** (se ainda não tiver)

**3. Criar Access Token:**
- Clique em seu app → **"Access Tokens"**
- **"Create Access Token"**
- **Permissões (IMPORTANTE - apenas leitura!)**:
  - ✅ `Reporting` (leitura de relatórios)
  - ✅ `Audience` (insights de audiência)
  - ❌ **NÃO** marque permissões de escrita (Campaign Management, etc.)

**4. Copiar credenciais:**
- **Access Token**: Formato `act.xxxxxxxxxxxxxxxx`
- **Advertiser ID**: Encontre em Settings → Advertiser Info

**5. Adicionar no `.env`:**
```bash
TIKTOK_ACCESS_TOKEN=act.xxxxxxxxxxxxxxxx
TIKTOK_ADVERTISER_ID=123456789
```

**6. Testar:**
```bash
cd analytics/scripts
python -c "from collectors.tiktok_collector import get_tiktok_metrics; print(get_tiktok_metrics())"
```

### Opção 2: TikTok Display API (para métricas orgânicas)

**Nota:** Requer aprovação do TikTok (1-2 dias)

**1. Solicitar acesso:**
- https://developers.tiktok.com/
- **"Apply for API Access"**
- Preencher formulário explicando uso

**2. Após aprovação:**
- Dashboard: https://developers.tiktok.com/apps
- Criar app e obter Client Key/Secret

**3. Configuração:**
```bash
TIKTOK_CLIENT_KEY=awxxxxxxxxxx
TIKTOK_CLIENT_SECRET=xxxxxxxxxxxxxxxx
```

**Nota:** Display API é mais complexa (requer OAuth 2.0)
**Recomendação:** Use n8n workflow para TikTok orgânico

### 🛡️ Segurança Extra

- ✅ Use permissões **read-only** apenas
- ✅ Rotacione tokens a cada 90 dias
- ✅ Monitore uso no dashboard
- **Se vazar**: Revogue token em https://ads.tiktok.com/marketing_api/apps

---

## 📋 Checklist Final

Após configurar tudo:

- [ ] ✅ Arquivo `.env` criado em `analytics/scripts/.env`
- [ ] ✅ APIs configuradas (apenas as que você vai usar)
- [ ] ✅ Limites de gasto configurados (OpenAI)
- [ ] ✅ Canais privados configurados (Slack)
- [ ] ✅ API Keys restritas (YouTube)
- [ ] ✅ Permissões read-only (TikTok)
- [ ] ✅ Testes executados com sucesso
- [ ] ✅ `.env` **NÃO** foi commitado no Git

### Verificar segurança:

```bash
# Verificar que .env está no .gitignore
git status --ignored | grep .env

# Deve mostrar:
# !!      .env
# !!      analytics/scripts/.env
```

---

## 🎓 Próximos Passos

Agora que tudo está configurado de forma segura:

1. **Testar coleta completa:**
```bash
cd analytics/scripts
python metrics-to-supabase.py
```

2. **Verificar dados no Supabase:**
- Dashboard: https://supabase.com/dashboard/project/zzpjqldhosgaxyjpcvqc
- Table Editor → `daily_metrics`

3. **Ver notificação no Slack:**
- Checar canal `#marketing-metrics-private`

4. **Monitorar custos:**
- OpenAI: https://platform.openai.com/usage
- YouTube: https://console.cloud.google.com/apis/dashboard (quota)

---

## ❓ FAQ

**P: Preciso configurar todos?**
R: Não! Comece com os que você vai usar. OpenAI e Slack são totalmente opcionais.

**P: Qual o custo mensal total?**
R:
- YouTube: Gratuito
- TikTok: Gratuito
- Slack: Gratuito
- OpenAI: ~$2-5/mês (se usar insights diários)

**P: E se eu não quiser pagar nada?**
R: Configure apenas YouTube, TikTok e Slack (todos gratuitos). Pule OpenAI.

**P: Como sei se minhas chaves estão seguras?**
R: Siga a checklist de segurança em [SECURITY-API-KEYS.md](../../docs/operations/SECURITY-API-KEYS.md)

---

## 🔗 Links Úteis

- **Guia de Segurança Completo:** [SECURITY-API-KEYS.md](../../docs/operations/SECURITY-API-KEYS.md)
- **OpenAI Dashboard:** https://platform.openai.com/
- **Slack API:** https://api.slack.com/
- **Google Cloud Console:** https://console.cloud.google.com/
- **TikTok for Business:** https://ads.tiktok.com/

---

**Precisando de ajuda?** Veja a documentação completa ou abra uma issue no GitHub.

**Última atualização:** 20 de Outubro, 2025
