# 🚀 GUIA DE DEPLOY FINAL
## Dashboard Sabrina Costa - Colocar no Ar

**Data:** 20 de Outubro de 2025  
**Status:** Pronto para Deploy  
**Tempo Estimado:** 1 hora

---

## ✅ PRÉ-REQUISITOS

Antes de começar, você precisa:
- [ ] Conta Vercel (https://vercel.com)
- [ ] Conta Supabase (https://supabase.com) ou Railway
- [ ] Acesso ao n8n (https://fluxos.macspark.dev)
- [ ] Evolution API configurada
- [ ] Git instalado

---

## 📋 PASSO 1: Configurar Banco de Dados (10 min)

### Opção A: Supabase (Recomendado - Grátis)

1. Acessar https://supabase.com
2. Criar novo projeto: "sabrina-costa"
3. Aguardar provisionamento (~2 min)
4. Ir em **SQL Editor**
5. Copiar todo conteúdo de `backend/db/schema.sql`
6. Colar no editor e executar
7. Copiar Connection String:
   - Ir em **Settings** → **Database**
   - Copiar **Connection String** (URI)
   - Trocar `[YOUR-PASSWORD]` pela senha real

**Connection String:**
```
postgresql://postgres.[REF]:[PASSWORD]@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

### Opção B: Railway ($5/mês)

1. Acessar https://railway.app
2. New Project → Provision PostgreSQL
3. Copiar connection string
4. Executar schema via CLI:
```bash
psql $DATABASE_URL < backend/db/schema.sql
```

---

## 📋 PASSO 2: Deploy Backend na Vercel (10 min)

### Via CLI:

```bash
cd sabrina-costa/backend

# Instalar Vercel CLI (se não tiver)
npm install -g vercel

# Deploy
vercel

# Seguir prompts:
# - Set up and deploy? Yes
# - Which scope? (sua conta)
# - Link to existing project? No
# - Project name: sabrina-costa-backend
# - Directory: ./
# - Override settings? No
```

### Configurar Variáveis de Ambiente:

No dashboard Vercel (https://vercel.com):
1. Ir no projeto → **Settings** → **Environment Variables**
2. Adicionar:

```
DATABASE_URL = sua_connection_string_do_supabase
JWT_SECRET = [gerar com: openssl rand -base64 32]
WEBHOOK_SECRET = [gerar com: openssl rand -base64 32]
CORS_ORIGIN = https://sabrina-costa.vercel.app
NODE_ENV = production
EVOLUTION_API_URL = https://evolution.macspark.dev
EVOLUTION_API_KEY = sua_chave_evolution
WHATSAPP_NUMBER = +5511999999999
WHATSAPP_INSTANCE = sabrina-instance
```

3. Fazer redeploy: **Deployments** → **...** → **Redeploy**

**URL do Backend:** https://sabrina-costa-backend.vercel.app

---

## 📋 PASSO 3: Deploy Frontend na Vercel (5 min)

```bash
cd sabrina-costa/frontend

# Deploy
vercel

# Seguir prompts:
# - Set up and deploy? Yes
# - Project name: sabrina-costa
# - Directory: ./
# - Override settings? No
```

### Atualizar API URL:

Editar `frontend/assets/js/api.js`:
```javascript
const API_CONFIG = {
    baseURL: 'https://sabrina-costa-backend.vercel.app/api',
    // ...
};
```

Fazer redeploy:
```bash
vercel --prod
```

**URL do Frontend:** https://sabrina-costa.vercel.app

---

## 📋 PASSO 4: Importar Workflows n8n (15 min)

### Via Interface Web:

1. Acessar https://fluxos.macspark.dev
2. Para cada workflow:
   - Click **Add workflow** → **Import from file**
   - Selecionar arquivo JSON de `n8n/workflows/`
   - Revisar e salvar

### Configurar Variáveis de Ambiente no n8n:

**Settings** → **Environment Variables**:
```
API_BASE_URL = https://sabrina-costa-backend.vercel.app
WEBHOOK_SECRET = mesmo_do_backend
DASHBOARD_URL = https://sabrina-costa.vercel.app
EVOLUTION_API_URL = https://evolution.macspark.dev
EVOLUTION_API_KEY = sua_chave
WHATSAPP_INSTANCE = sabrina-instance
WHATSAPP_NUMBER = +5511999999999
TZ = America/Sao_Paulo
```

### Ativar Workflows:

Para cada workflow importado:
1. Abrir workflow
2. Click **Active** (toggle no topo)
3. Testar manualmente (botão Execute)

---

## 📋 PASSO 5: Testes End-to-End (20 min)

### Teste 1: Login
```
1. Abrir https://sabrina-costa.vercel.app
2. Fazer login:
   Email: gerente@macspark.dev
   Senha: Sabrina2025!
3. Verificar redirecionamento para dashboard
```

### Teste 2: Dashboard
```
1. Verificar se gráficos carregam
2. Verificar se KPIs aparecem
3. Navegar entre páginas
```

### Teste 3: Enviar Métricas
```bash
# Via n8n webhook
curl -X POST https://fluxos.macspark.dev/webhook/sabrina/metricas \
  -H "X-Webhook-Token: seu_webhook_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-10-21",
    "ctr": 7.5,
    "cpc": 0.09,
    "cost": 20.00,
    "newFollowers": 50
  }'
```

Verificar:
- [ ] Dados aparecem no dashboard
- [ ] Workflow executou sem erros

### Teste 4: Alertas WhatsApp
```
1. Enviar métrica com CTR < 1.5%
2. Aguardar 18h ou executar workflow 2 manualmente
3. Verificar se recebeu WhatsApp
```

### Teste 5: Relatório Diário
```
1. Executar workflow 3 manualmente
2. Verificar WhatsApp recebido
```

---

## ✅ CHECKLIST FINAL DE DEPLOY

### Banco de Dados
- [ ] Supabase/Railway provisionado
- [ ] Schema SQL executado
- [ ] Seed data inserido
- [ ] Connection string copiada

### Backend
- [ ] Deploy Vercel concluído
- [ ] Variáveis de ambiente configuradas
- [ ] Health check respondendo: `/api/health`
- [ ] Login funcionando: `/api/auth/login`

### Frontend
- [ ] Deploy Vercel concluído
- [ ] API_URL atualizada
- [ ] Login abrindo
- [ ] Dashboard carregando

### n8n
- [ ] 4 workflows importados
- [ ] Variáveis configuradas
- [ ] Workflows ativados
- [ ] Webhook testado
- [ ] Evolution API conectada

### Testes
- [ ] Login funciona
- [ ] Dashboard carrega métricas
- [ ] Envio de métricas funciona
- [ ] Alertas WhatsApp funcionam
- [ ] Relatórios chegam
- [ ] Todas páginas acessíveis

---

## 🆘 TROUBLESHOOTING

### Erro: "Database connection failed"
```bash
# Testar connection string
psql "sua_connection_string_aqui"

# Verificar se variável está no Vercel
```

### Erro: "Webhook 404"
```bash
# Verificar se workflow está ativo no n8n
# Verificar path: /webhook/sabrina/metricas
# Verificar X-Webhook-Token
```

### Erro: "CORS error"
```bash
# Adicionar frontend URL no CORS_ORIGIN do backend
# Redeploy backend
```

---

## 🎉 APÓS DEPLOY COMPLETO

**URLs Finais:**
- 🎨 Frontend: https://sabrina-costa.vercel.app
- ⚙️ Backend: https://sabrina-costa-backend.vercel.app
- 🤖 n8n: https://fluxos.macspark.dev
- 📊 Status: https://sabrina-costa-backend.vercel.app/api/health

**Credenciais:**
- Email: gerente@macspark.dev
- Senha: Sabrina2025!

**Próximos Passos:**
1. Compartilhar URL com Sabrina
2. Treinar uso do dashboard
3. Começar a enviar métricas diárias
4. Monitorar alertas WhatsApp

---

**Projeto 100% no ar e funcionando! 🌟**

