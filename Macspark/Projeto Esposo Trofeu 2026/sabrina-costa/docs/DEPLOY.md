# Guia de Deploy – Projeto Sabrina Costa

> Última revisão: 2025-01-05  
> Responsável: Squad Macspark Growth Ops

Este documento consolida os passos necessários para colocar o projeto em produção (frontend, backend, banco de dados e automações n8n), além de testes e checklists pós-deploy.

---

## 1. Visão Geral

| Camada      | Stack / Serviço             | Observações                                               |
|-------------|-----------------------------|-----------------------------------------------------------|
| Frontend    | HTML + Tailwind (static)    | Deploy recomendado na Vercel (Static Site)               |
| Backend API | Node.js + Express           | Deploy recomendado na Render / Fly.io                    |
| Banco       | PostgreSQL (Supabase)       | Schema em `backend/db/schema.sql`                        |
| Automação   | n8n Cloud (fluxos.macspark) | Workflows prontos em `n8n/workflows/*.json`              |
| Alertas     | Evolution API (WhatsApp)    | Autenticação via `apikey`                                |

---

## 2. Backend API

### 2.1 Pré-requisitos

```bash
cd backend
npm install
npm run dev        # validação local (necessário PostgreSQL disponível)
```

> **Dica:** use `docker-compose up db` (arquivo exemplo em backlog) ou uma instância Supabase local para testes.

### 2.2 Variáveis de ambiente obrigatórias

- Copiar `backend/env.example` ➜ `backend/.env`
- Ajustar:
  - `DATABASE_URL`
  - `JWT_SECRET`
  - `API_SERVICE_TOKEN` (token JWT utilizado pelas automações)
  - `WEBHOOK_SECRET`
  - Credenciais Evolution API (`EVOLUTION_API_*`)

### 2.3 Migração do banco

```bash
psql $DATABASE_URL -f db/schema.sql
```

> Executa estrutura + seed (admin, hooks, posts). Reaplica sem problemas graças a `CREATE IF NOT EXISTS`.

### 2.4 Deploy

1. Criar serviço na Render ou plataforma similar (Node 18+).
2. Build command: `npm install`
3. Start command: `npm run start`
4. Definir variáveis de ambiente (copiar do `.env`).
5. Liberar CORS para o domínio da Vercel (`CORS_ORIGIN`).

### 2.5 Smoke Tests

- `curl https://api-url/api/health`
- `curl -X POST /api/auth/login` (usar credenciais seed)
- `curl -H "Authorization: Bearer <token>" /api/metrics`

---

## 3. Frontend (Static)

### 3.1 Estrutura

- HTMLs em `frontend/`
- Assets (CSS/JS) em `frontend/assets/`
- Dependências via CDN ➜ zero build step

### 3.2 Deploy Vercel

1. Criar projeto Vercel (Framework: **Other / Static**).
2. Pasta pública: `frontend`.
3. Build command: _em branco_ (site estático).
4. Definir `rewrites` (opcional) para servir `index.html` como login.

### 3.3 Pós-deploy

- Validar login (`index.html`) e dashboard (`dashboard.html`).
- Conferir novas páginas:
  - `cronograma.html`
  - `ganchos.html`
  - `checklist.html`
  - `relatorios.html`
  - `configuracoes.html`
- Inspecionar console do navegador (erros de CORS/401).

---

## 4. n8n Workflows

### 4.1 Importação

Na interface n8n (`https://fluxos.macspark.dev`):

1. `Workflows > Import from File`.
2. Importar cada JSON de `n8n/workflows/`:
   - `01-processar-metricas.json`
   - `02-alertas-whatsapp.json`
   - `03-relatorio-diario.json`
   - `04-lembretes-postagem.json`
3. Revisar credenciais ➜ selecionar `HTTP Header Auth` com `API_SERVICE_TOKEN`.
4. Ativar cada workflow.

### 4.2 Variáveis de ambiente n8n

Adicionar em **Settings → Environments**:

```
API_BASE_URL=https://seu-backend.com
API_TOKEN=<API_SERVICE_TOKEN>
WEBHOOK_SECRET=mesmo_do_backend
EVOLUTION_API_URL=https://evolution.macspark.dev
EVOLUTION_API_KEY=<sua_api_key>
WHATSAPP_INSTANCE=sabrina-instance
WHATSAPP_NUMBER=+5511999999999
DASHBOARD_URL=https://seu-frontend.vercel.app
```

### 4.3 Testes

- Workflow 1: enviar POST para `/webhook/sabrina/metricas` com payload JSON.
- Workflow 2/3: usar botão **Execute Workflow** (substitui cron).
- Workflow 4: alterar temporariamente hora do cron (por exemplo, +2 min) para validar.

---

## 5. Evolution API (WhatsApp)

### 5.1 Checklist

- Instância ativa (`WHATSAPP_INSTANCE`).
- Número autenticado.
- Teste rápido:

```bash
curl -X POST $EVOLUTION_API_URL/message/sendText/$WHATSAPP_INSTANCE \
  -H "apikey: $EVOLUTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"number":"+5511999999999","text":"Teste Macspark Sabrina"}'
```

---

## 6. Testes e Observabilidade

### 6.1 Testes locais (backend)

```bash
npm test          # Jest (placeholder, adicionar suites)
node server.js    # smoke manual (usar Thunder Client/Postman)
```

### 6.2 Health Checks pós-deploy

1. `GET /api/health` ➜ status 200.
2. `POST /api/auth/login` ➜ retorno token.
3. `GET /api/metrics` com token ➜ retorna lista.
4. `POST /api/webhook/metrics` ➜ responde `success: true`.

### 6.3 Monitoramento

- Ativar logs HTTP (Render) e alertas de erro (Sentry opcional).
- n8n ➜ Configurar notificações de falha nas execuções.

---

## 7. Pós-Deploy Checklist

- [ ] Ambiente `.env` versionado de forma segura (1Password / Doppler).
- [ ] Workflows n8n ativados e com logs verdes.
- [ ] Evolution API respondendo com `200`.
- [ ] Dashboard público atualizado.
- [ ] Documentação atualizada (`docs/DEPLOY.md`, `docs/API-SPEC.md` se necessário).
- [ ] Comunicar squad + cliente com URL final e possíveis próximos passos.

---

## 8. Próximos Incrementos (Backlog)

- Automatizar pipeline CI (GitHub Actions) com lint/test.
- Adicionar coverage mínimo Jest (auth + metrics).
- Provisionar infraestrutura IaC (Terraform) para Render + Supabase.
- Integrar monitoramento (Statuspage / Better Uptime) para API e workflows.

---

> **Contato Time Ops:** `ops@macspark.dev` – Slack `#ops-sabrina`
