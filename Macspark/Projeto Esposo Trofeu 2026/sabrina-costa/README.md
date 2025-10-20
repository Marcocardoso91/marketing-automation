# 🌟 Dashboard Sabrina Costa

**Projeto completo de gerenciamento e automação para crescimento no Instagram**

[![Status](https://img.shields.io/badge/status-em_desenvolvimento-yellow)](https://github.com)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Deploy](#deploy)
- [Uso](#uso)
- [n8n Workflows](#n8n-workflows)
- [API Documentation](#api-documentation)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

Dashboard completo para gerenciar o projeto de crescimento da Sabrina Costa no Instagram, incluindo:

✅ **Dashboard executivo** com métricas em tempo real  
✅ **Sistema de automação** com n8n  
✅ **Alertas via WhatsApp** quando métricas fora do padrão  
✅ **Cronograma visual** de posts (4 semanas)  
✅ **Biblioteca de 50 ganchos virais**  
✅ **Checklist interativo** de produção  
✅ **Relatórios automáticos** diários  
✅ **API REST** completa  
✅ **Autenticação JWT** com login seguro  

---

## 🚀 Tecnologias

### Frontend
- **HTML5** + **Tailwind CSS 3.4** - Interface moderna e responsiva
- **Alpine.js 3.x** - Reatividade leve e performática
- **Chart.js 4.x** - Gráficos interativos e bonitos
- **Day.js** - Manipulação de datas

### Backend
- **Node.js 18+** + **Express 4.x** - API REST
- **PostgreSQL 15** - Banco de dados relacional
- **JWT** - Autenticação segura
- **bcryptjs** - Hash de senhas

### Automação
- **n8n** (https://fluxos.macspark.dev) - 4 workflows automatizados
- **Evolution API** - Integração WhatsApp

### Infraestrutura
- **Vercel** - Deploy frontend + serverless functions
- **Supabase/Railway** - Banco PostgreSQL hospedado
- **GitHub** - Versionamento de código

---

## 📁 Estrutura do Projeto

```
sabrina-costa/
├── docs/                          # 📚 Documentação completa
│   ├── PRD.md                     # Product Requirements Document
│   ├── ARQUITETURA.md             # Arquitetura do sistema
│   ├── API-SPEC.md                # Especificação da API REST
│   └── N8N-WORKFLOWS.md           # Documentação dos workflows
│
├── frontend/                      # 🎨 Interface web
│   ├── index.html                 # Página de login
│   ├── dashboard.html             # Dashboard principal
│   ├── cronograma.html            # Timeline de posts
│   ├── ganchos.html               # Biblioteca de ganchos
│   ├── checklist.html             # Checklist de produção
│   ├── relatorios.html            # Relatórios semanais
│   ├── configuracoes.html         # Configurações
│   ├── assets/
│   │   ├── css/
│   │   │   └── styles.css         # Estilos customizados
│   │   ├── js/
│   │   │   ├── api.js             # Cliente HTTP
│   │   │   ├── auth.js            # Autenticação
│   │   │   ├── dashboard.js       # Lógica do dashboard
│   │   │   └── main.js            # Utilitários gerais
│   │   └── img/                   # Imagens e logos
│   └── vercel.json                # Config deploy Vercel
│
├── backend/                       # ⚙️ API REST
│   ├── api/
│   │   ├── auth.js                # Endpoints de autenticação
│   │   ├── metrics.js             # Endpoints de métricas
│   │   ├── webhook.js             # Webhook receiver (n8n)
│   │   └── alerts.js              # Endpoints de alertas
│   ├── db/
│   │   ├── schema.sql             # Schema do banco
│   │   └── connection.js          # Conexão PostgreSQL
│   ├── utils/
│   │   └── jwt.js                 # Utilitários JWT
│   ├── package.json               # Dependências Node.js
│   └── .env.example               # Exemplo de variáveis

├── n8n/                           # 🤖 Workflows de automação
│   ├── workflows/
│   │   ├── 01-receber-metricas.json
│   │   ├── 02-alertas-whatsapp.json
│   │   ├── 03-relatorio-diario.json
│   │   └── 04-lembretes-postagem.json
│   └── README-N8N.md              # Instruções de importação
│
└── README.md                      # Este arquivo
```

---

## 💻 Instalação

### Pré-requisitos

- **Node.js 18+** instalado
- **PostgreSQL 15+** ou conta Supabase/Railway
- **n8n** instalado e configurado
- **Evolution API** configurada (para WhatsApp)
- Conta **Vercel** (para deploy)

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd setup-macspark
```

### 2. Instalar Dependências Backend

```bash
cd backend
npm install
```

### 3. Configurar Banco de Dados

```bash
# Criar banco de dados
createdb sabrina_dashboard

# Executar schema
psql sabrina_dashboard < db/schema.sql
```

Ou use Supabase:
1. Criar projeto em https://supabase.com
2. Copiar connection string
3. Executar schema via SQL Editor

### 4. Configurar Variáveis de Ambiente

```bash
# Backend
cd backend
cp .env.example .env
# Editar .env com suas credenciais
```

**Exemplo `.env`:**
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sabrina_dashboard

# JWT
JWT_SECRET=super_secret_key_change_in_production
JWT_EXPIRES_IN=7d

# API
PORT=3000
NODE_ENV=development

# Webhook
WEBHOOK_SECRET=webhook_secret_token_here

# CORS
CORS_ORIGIN=http://localhost:3000,https://dashboard-sabrina.vercel.app

# Evolution API
EVOLUTION_API_URL=https://evolution.macspark.dev
EVOLUTION_API_KEY=your_evolution_api_key
WHATSAPP_NUMBER=+5511999999999
```

### 5. Configurar n8n

Ver [docs/N8N-WORKFLOWS.md](docs/N8N-WORKFLOWS.md) para instruções detalhadas.

**Resumo:**
1. Acessar https://fluxos.macspark.dev
2. Importar 4 workflows JSON de `n8n/workflows/`
3. Configurar variáveis de ambiente no n8n
4. Ativar workflows

---

## ⚙️ Configuração

### Criar Usuário Admin

```bash
cd backend
npm run create-admin
# Seguir instruções para criar usuário
```

Ou inserir manualmente no banco:

```sql
INSERT INTO users (email, password_hash, name, role) VALUES
('gerente@macspark.dev', '$2a$10$hashedpassword', 'Marco', 'admin');
```

Use bcrypt para gerar hash da senha:
```bash
node -e "console.log(require('bcryptjs').hashSync('Sabrina2025!', 10))"
```

### Povoar Dados Iniciais

```bash
cd backend
npm run seed
```

Isso irá:
- Inserir 50 ganchos virais
- Inserir cronograma de 4 semanas (30 posts)
- Inserir configurações padrão

---

## 🚀 Deploy

### Frontend (Vercel)

1. **Via GitHub:**
   - Conectar repositório no Vercel
   - Definir root directory: `sabrina-costa/frontend`
   - Deploy automático

2. **Via CLI:**
```bash
cd frontend
npm install -g vercel
vercel
```

3. **Configurar Variáveis de Ambiente no Vercel:**
   - `API_BASE_URL`: URL da API backend
   - Outros conforme necessário

### Backend (Vercel Serverless Functions)

```bash
cd backend
vercel
```

**Ou Railway:**
```bash
railway login
railway init
railway up
```

### Configurações Importantes

**Vercel (frontend):**
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://api.dashboard-sabrina.com/api/$1" }
  ]
}
```

**Variáveis de Ambiente (Production):**
- DATABASE_URL
- JWT_SECRET (gerar novo com: `openssl rand -base64 32`)
- WEBHOOK_SECRET (gerar novo)
- EVOLUTION_API_KEY
- Etc.

---

## 📱 Uso

### Acessar Dashboard

1. Abrir navegador: `https://dashboard-sabrina.vercel.app`
2. Fazer login com credenciais:
   - Email: `gerente@macspark.dev`
   - Senha: `Sabrina2025!`
3. Navegar pelas páginas

### Atualizar Métricas Manualmente

**Via Webhook (curl):**
```bash
curl -X POST https://fluxos.macspark.dev/webhook/sabrina/metricas \
  -H "X-Webhook-Token: seu_webhook_token" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-10-21",
    "ctr": 7.5,
    "cpc": 0.09,
    "cpm": 2.0,
    "frequency": 0.98,
    "visits": 90,
    "newFollowers": 50,
    "cost": 20.00,
    "impressions": 1200,
    "clicks": 90
  }'
```

**Via CSV:**
```bash
curl -X POST https://fluxos.macspark.dev/webhook/sabrina/metricas/csv \
  -H "X-Webhook-Token: seu_webhook_token" \
  -H "Content-Type: text/csv" \
  --data-binary @metricas.csv
```

### Workflows Automáticos

- **Workflow 1** (Processar Métricas): Dispara quando você envia métricas
- **Workflow 2** (Alertas): Roda às 18h diariamente
- **Workflow 3** (Relatório): Roda às 18h05 diariamente
- **Workflow 4** (Lembretes): Roda às 11h e 17h30 diariamente

---

## 🤖 n8n Workflows

### Workflow 1: Processar Métricas
- **Trigger:** Webhook POST
- **Função:** Recebe CSV/JSON, valida, salva no banco, verifica thresholds, dispara alertas
- **Arquivo:** `n8n/workflows/01-receber-metricas.json`

### Workflow 2: Alertas WhatsApp
- **Trigger:** Cron (18:00 diariamente)
- **Função:** Verifica métricas do dia, compara com thresholds, envia alertas via WhatsApp
- **Arquivo:** `n8n/workflows/02-alertas-whatsapp.json`

### Workflow 3: Relatório Diário
- **Trigger:** Cron (18:05 diariamente)
- **Função:** Compila métricas, calcula comparações, envia relatório formatado via WhatsApp
- **Arquivo:** `n8n/workflows/03-relatorio-diario.json`

### Workflow 4: Lembretes de Postagem
- **Trigger:** Cron (11:00 e 17:30)
- **Função:** Verifica posts do dia, envia lembrete com hook e CTA via WhatsApp
- **Arquivo:** `n8n/workflows/04-lembretes-postagem.json`

**Documentação completa:** [docs/N8N-WORKFLOWS.md](docs/N8N-WORKFLOWS.md)

---

## 📖 API Documentation

Documentação completa da API REST: [docs/API-SPEC.md](docs/API-SPEC.md)

**Endpoints principais:**

```
POST /api/auth/login        - Autenticar usuário
GET  /api/metrics           - Listar métricas
POST /api/metrics           - Criar métrica
GET  /api/schedule          - Listar cronograma
PUT  /api/schedule/:id      - Atualizar post
GET  /api/alerts            - Listar alertas
POST /api/webhook/metrics   - Receber métricas (n8n)
```

**Exemplo de uso:**
```javascript
// Login
const response = await fetch('https://api.dashboard-sabrina.com/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'gerente@macspark.dev',
    password: 'Sabrina2025!'
  })
});

const { token } = await response.json();

// Get metrics
const metrics = await fetch('https://api.dashboard-sabrina.com/api/metrics?period=7d', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

---

## 🧪 Testes

### Rodar Testes Backend

```bash
cd backend
npm test
```

### Testar Workflows n8n

1. Acessar https://fluxos.macspark.dev
2. Abrir workflow
3. Clicar em "Execute Workflow" (botão play)
4. Verificar output de cada node

### Testar Frontend Local

```bash
cd frontend
# Abrir index.html em um servidor local
python -m http.server 8000
# ou
npx serve
```

---

## 🐛 Troubleshooting

### Erro: "Sessão expirada"
- Token JWT expirou (7 dias de validade)
- Fazer login novamente

### Erro: "Webhook não recebe dados"
- Verificar se n8n está online
- Verificar `X-Webhook-Token` header
- Ver logs no n8n: Executions → Ver detalhes

### Erro: "Evolution API não envia WhatsApp"
- Verificar se Evolution API está online
- Testar endpoint diretamente (curl)
- Verificar `EVOLUTION_API_KEY` e número de WhatsApp

### Erro: "Database connection failed"
- Verificar `DATABASE_URL` no `.env`
- Verificar se PostgreSQL está rodando
- Testar conexão: `psql $DATABASE_URL`

---

## 📚 Documentação Adicional

- [PRD (Product Requirements)](docs/PRD.md)
- [Arquitetura do Sistema](docs/ARQUITETURA.md)
- [API Specification](docs/API-SPEC.md)
- [n8n Workflows](docs/N8N-WORKFLOWS.md)

---

## 🤝 Contribuindo

1. Fork o projeto
2. Criar branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abrir Pull Request

---

## 📝 Licença

Este projeto é propriedade de **Macspark** e está sob licença privada.

---

## 👥 Equipe

- **Marco** - Product Owner & Tech Lead
- **Sabrina** - Cliente & Usuária

---

## 📞 Suporte

- **Email:** suporte@macspark.dev
- **WhatsApp:** +55 11 99999-9999
- **Documentação:** https://docs.dashboard-sabrina.com

---

## ✅ Checklist de Deploy

- [ ] Banco de dados criado e schema aplicado
- [ ] Usuário admin criado
- [ ] Dados iniciais inseridos (ganchos, cronograma)
- [ ] Variáveis de ambiente configuradas
- [ ] Frontend deployado na Vercel
- [ ] Backend deployado (Vercel/Railway)
- [ ] n8n workflows importados e ativos
- [ ] Evolution API testada e funcionando
- [ ] Primeiro envio de métricas testado
- [ ] Alertas WhatsApp testados
- [ ] Login funcionando
- [ ] Dashboard carregando métricas
- [ ] Documentação revisada

---

## 🎉 Próximos Passos

- [ ] Integração com Google Sheets (sincronização automática)
- [ ] Notificações push no dashboard
- [ ] Exportar relatórios em PDF
- [ ] App mobile (React Native)
- [ ] Análise preditiva com IA
- [ ] Múltiplos clientes/projetos
- [ ] Dashboard público para cliente (view-only)

---

**Última Atualização:** 20 de Outubro de 2025  
**Versão:** 1.0.0  
**Status:** Em Desenvolvimento → Produção

---

🌟 **Feito com ❤️ pela equipe Macspark**

