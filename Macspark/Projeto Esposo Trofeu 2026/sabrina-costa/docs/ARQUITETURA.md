# Arquitetura do Sistema
## Dashboard Sabrina Costa + Automação n8n

**Versão:** 1.0  
**Data:** 20 de Outubro de 2025

---

## 1. VISÃO GERAL DA ARQUITETURA

### 1.1 Diagrama de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                          USUÁRIOS                                │
│         (Gerente, Sabrina, Equipe)                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VERCEL CDN + FRONTEND                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Dashboard   │  │  Cronograma  │  │   Ganchos    │         │
│  │  (HTML/JS)   │  │  (HTML/JS)   │  │  (HTML/JS)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│          │                  │                  │                 │
│          └──────────────────┴──────────────────┘                │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │ REST API (HTTPS)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              VERCEL SERVERLESS FUNCTIONS                         │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ /api/auth  │  │/api/metrics │  │/api/webhook │             │
│  │  (Login)   │  │ (CRUD)      │  │ (n8n recv)  │             │
│  └─────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│        │                 │                 │                     │
└────────┼─────────────────┼─────────────────┼─────────────────────┘
         │                 │                 │
         │        ┌────────▼─────────┐      │
         │        │                  │      │
         │        │   SUPABASE /     │      │
         └───────►│   POSTGRESQL     │◄─────┘
                  │   (Database)     │
                  │                  │
                  └───────▲──────────┘
                          │
                          │ HTTP REST
                          │
┌─────────────────────────┴───────────────────────────────────────┐
│                   n8n AUTOMATION ENGINE                          │
│               (https://fluxos.macspark.dev)                      │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 1: Processar Métricas                           │  │
│  │ Webhook → Parse CSV → Validate → Save DB → Alert Check  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 2: Alertas WhatsApp                             │  │
│  │ Cron (18h) → Get Metrics → Check Thresholds → WhatsApp  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 3: Relatório Diário                             │  │
│  │ Cron (18h) → Compile Data → Format → Send WhatsApp      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 4: Lembretes Postagem                           │  │
│  │ Cron (multi) → Check Schedule → Send Reminder           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │ HTTP API
                           ▼
                 ┌──────────────────────┐
                 │   Evolution API      │
                 │   (WhatsApp)         │
                 │                      │
                 └──────────┬───────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   WhatsApp    │
                    │   (Sabrina)   │
                    └───────────────┘
```

---

## 2. CAMADAS DA APLICAÇÃO

### 2.1 Camada de Apresentação (Frontend)

#### Tecnologias
- **HTML5**: Estrutura semântica
- **Tailwind CSS 3.4**: Framework CSS utilitário
- **Alpine.js 3.x**: Framework JavaScript reativo leve
- **Chart.js 4.x**: Biblioteca de gráficos
- **Axios**: Cliente HTTP

#### Responsabilidades
- Renderizar interface do usuário
- Capturar interações do usuário
- Fazer requisições para API backend
- Gerenciar estado local (login, cache)
- Exibir feedback visual (loading, erros, sucesso)

#### Estrutura de Páginas

```
frontend/
├── index.html              # Landing + Login
├── dashboard.html          # Dashboard principal com KPIs
├── cronograma.html         # Timeline de posts
├── ganchos.html            # Biblioteca de ganchos virais
├── checklist.html          # Checklist de produção
├── relatorios.html         # Relatórios semanais
└── configuracoes.html      # Configurações de alertas e metas
```

#### Fluxo de Autenticação

```
1. Usuário acessa index.html
2. Preenche email + senha
3. JavaScript envia POST /api/auth/login
4. Backend valida e retorna JWT
5. Frontend salva JWT no localStorage
6. Redireciona para dashboard.html
7. Cada página verifica JWT antes de carregar
8. Se JWT inválido/expirado → redireciona para login
```

### 2.2 Camada de Aplicação (Backend API)

#### Tecnologias
- **Node.js 18+**: Runtime JavaScript
- **Express 4.x**: Framework web minimalista
- **jsonwebtoken**: Geração e validação de JWT
- **bcryptjs**: Hash de senhas
- **pg**: Cliente PostgreSQL
- **cors**: Middleware CORS
- **helmet**: Security headers

#### Endpoints

##### Autenticação
```
POST /api/auth/login
├── Body: { email, password }
├── Valida credenciais
├── Gera JWT (exp: 7 dias)
└── Retorna: { token, user: { id, name, email } }

POST /api/auth/logout
├── Headers: Authorization: Bearer <token>
├── Invalida token (blacklist)
└── Retorna: { success: true }

GET /api/auth/me
├── Headers: Authorization: Bearer <token>
├── Valida JWT
└── Retorna: { user: { id, name, email } }
```

##### Métricas
```
GET /api/metrics
├── Headers: Authorization: Bearer <token>
├── Query: ?date=YYYY-MM-DD&period=7d
├── Busca métricas do banco
└── Retorna: [{ date, ctr, cpc, cpm, ... }]

POST /api/metrics
├── Headers: Authorization: Bearer <token>
├── Body: { date, ctr, cpc, cpm, frequency, ... }
├── Valida dados
├── Insere no banco
└── Retorna: { id, ...dados }

PUT /api/metrics/:id
├── Headers: Authorization: Bearer <token>
├── Body: { campos_a_atualizar }
├── Atualiza registro
└── Retorna: { id, ...dados_atualizados }
```

##### Webhook (para n8n)
```
POST /api/webhook/metrics
├── Headers: X-Webhook-Token: <secret>
├── Body: { date, ctr, cpc, ... } ou CSV
├── Parse e validação
├── Insere no banco
├── Verifica thresholds para alertas
└── Retorna: { success, saved_records }
```

##### Cronograma
```
GET /api/schedule
├── Headers: Authorization: Bearer <token>
├── Query: ?week=1&status=planned
├── Busca posts do banco
└── Retorna: [{ date, format, theme, hook, cta, status }]

PUT /api/schedule/:id
├── Headers: Authorization: Bearer <token>
├── Body: { status: 'posted' }
├── Atualiza status do post
└── Retorna: { id, ...dados }
```

##### Alertas
```
GET /api/alerts
├── Headers: Authorization: Bearer <token>
├── Query: ?limit=10
├── Busca alertas recentes
└── Retorna: [{ type, message, sent_at, status }]

POST /api/alerts
├── Headers: Authorization: Bearer <token> ou X-Webhook-Token
├── Body: { type, message }
├── Insere alerta
└── Retorna: { id, ...dados }

PUT /api/alerts/config
├── Headers: Authorization: Bearer <token>
├── Body: { ctr_min, cpc_max, whatsapp_number, ... }
├── Atualiza configurações
└── Retorna: { success }
```

#### Middleware Pipeline

```
Request
  │
  ├── helmet (security headers)
  ├── cors (CORS config)
  ├── express.json() (parse JSON)
  │
  ├── authenticateJWT (verifica token)
  │     │
  │     ├─ Token válido? → next()
  │     └─ Token inválido? → 401 Unauthorized
  │
  ├── validateInput (valida body/query)
  │     │
  │     ├─ Dados válidos? → next()
  │     └─ Dados inválidos? → 400 Bad Request
  │
  ├── Controller (lógica de negócio)
  │     │
  │     ├─ Sucesso → 200/201
  │     └─ Erro → 4xx/5xx
  │
  └── errorHandler (captura erros)
        │
        └─ Log + Resposta formatada
```

### 2.3 Camada de Dados (Database)

#### Tecnologia
- **PostgreSQL 15**: Banco relacional
- **Supabase** ou **Railway**: Hospedagem gerenciada

#### Schema

```sql
-- Tabela de usuários
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer', -- 'admin', 'viewer'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de métricas do Instagram
CREATE TABLE metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL UNIQUE,
    ctr DECIMAL(5,2), -- Click-Through Rate (%)
    cpc DECIMAL(10,2), -- Custo Por Clique (R$)
    cpm DECIMAL(10,2), -- Custo Por Mil Impressões (R$)
    frequency DECIMAL(5,2), -- Frequência de exibição
    visits INTEGER, -- Visitas ao perfil
    new_followers INTEGER, -- Novos seguidores
    cost DECIMAL(10,2), -- Investimento do dia (R$)
    impressions INTEGER, -- Impressões totais
    clicks INTEGER, -- Cliques totais
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_metrics_date ON metrics(date DESC);

-- Tabela de alertas
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL, -- 'ctr_low', 'cpc_high', 'frequency_high', etc
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'sent', -- 'sent', 'pending', 'failed'
    metadata JSONB, -- Dados extras (valores que geraram alerta)
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alerts_sent_at ON alerts(sent_at DESC);

-- Tabela de posts/cronograma
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    week_number INTEGER NOT NULL, -- 1, 2, 3, 4
    format VARCHAR(50) NOT NULL, -- 'reel', 'carousel', 'stories'
    theme VARCHAR(255) NOT NULL,
    hook TEXT,
    cta TEXT,
    objective VARCHAR(100),
    stories_ideas TEXT,
    status VARCHAR(20) DEFAULT 'planned', -- 'planned', 'posted', 'cancelled'
    posted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_posts_date ON posts(date);
CREATE INDEX idx_posts_status ON posts(status);

-- Tabela de ganchos virais
CREATE TABLE hooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category VARCHAR(100) NOT NULL, -- 'Curiosidade', 'Urgência', etc
    text TEXT NOT NULL,
    usage_count INTEGER DEFAULT 0, -- Quantas vezes foi usado
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_hooks_category ON hooks(category);

-- Tabela de configurações
CREATE TABLE config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Inserir configurações padrão
INSERT INTO config (key, value) VALUES
('thresholds', '{
    "ctr_min": 1.5,
    "cpc_max": 0.70,
    "cpm_max": 10.0,
    "frequency_max": 3.0,
    "cost_per_follower_max": 1.30
}'::jsonb),
('whatsapp', '{
    "number": "+5511999999999",
    "enabled": true
}'::jsonb),
('alerts_schedule', '{
    "daily_report": "18:00",
    "post_reminders": ["11:00", "17:30"]
}'::jsonb);
```

#### Queries Otimizadas

```sql
-- Buscar métricas dos últimos 30 dias
SELECT * FROM metrics 
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date DESC;

-- Buscar métricas do dia
SELECT * FROM metrics 
WHERE date = CURRENT_DATE;

-- Calcular média de CTR da semana
SELECT AVG(ctr) as avg_ctr 
FROM metrics 
WHERE date >= CURRENT_DATE - INTERVAL '7 days';

-- Posts pendentes do dia
SELECT * FROM posts 
WHERE date = CURRENT_DATE 
  AND status = 'planned'
ORDER BY date;

-- Últimos 10 alertas
SELECT * FROM alerts 
ORDER BY sent_at DESC 
LIMIT 10;
```

### 2.4 Camada de Automação (n8n)

#### Workflow 1: Processar Métricas

```
┌─────────────────────┐
│  Webhook Trigger    │ (POST com CSV ou JSON)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Parse Data         │ (CSV → JSON ou JSON validação)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Validate Fields    │ (Check required fields)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Calculate Derived  │ (Ex: custo_por_seguidor = cost/new_followers)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │ (POST /api/webhook/metrics)
└──────────┬──────────┘
           │
           ├─── Success ────┐
           │                 │
           │                 ▼
           │        ┌─────────────────────┐
           │        │  Check Thresholds   │
           │        └──────────┬──────────┘
           │                   │
           │                   ├─── Alert needed? ─┐
           │                   │                     │
           │                   │                     ▼
           │                   │            ┌─────────────────┐
           │                   │            │  Send Alert     │
           │                   │            └─────────────────┘
           │                   │
           │                   └─── No alert ─┐
           │                                   │
           │                                   ▼
           │                          ┌─────────────────┐
           │                          │  Log Success    │
           │                          └─────────────────┘
           │
           └─── Error ────┐
                          │
                          ▼
                 ┌─────────────────┐
                 │  Log Error      │
                 │  Send Alert     │
                 └─────────────────┘
```

#### Workflow 2: Alertas WhatsApp

```
┌─────────────────────┐
│  Cron (18:00)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │ (GET /api/metrics?date=today)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Get Config         │ (GET /api/config/thresholds)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Function Node      │ (Check each threshold)
│  Check Thresholds   │  - CTR < 1.5%?
│                     │  - CPC > R$0.70?
│                     │  - Frequency > 3.0?
└──────────┬──────────┘
           │
           ├─── No alerts ───┐
           │                  │
           │                  ▼
           │         ┌─────────────────┐
           │         │  End (no action)│
           │         └─────────────────┘
           │
           └─── Has alerts ──┐
                             │
                             ▼
                    ┌─────────────────────┐
                    │  Format Message     │
                    │  (Template string)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  HTTP Request       │
                    │  (Evolution API)    │
                    │  Send WhatsApp      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  HTTP Request       │
                    │  POST /api/alerts   │
                    │  (Log alert)        │
                    └─────────────────────┘
```

#### Workflow 3: Relatório Diário

```
┌─────────────────────┐
│  Cron (18:00)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │ (GET /api/metrics?date=today)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │ (GET /api/metrics?date=yesterday)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Function Node      │
│  Calculate:         │
│  - Comparisons      │
│  - Status (good/bad)│
│  - Recommendations  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Function Node      │
│  Format Report      │
│  (Markdown template)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │
│  Evolution API      │
│  Send WhatsApp      │
└─────────────────────┘
```

#### Workflow 4: Lembretes de Postagem

```
┌─────────────────────┐
│  Cron (11:00)       │ (Para posts meio-dia)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  HTTP Request       │ (GET /api/schedule?date=today&status=planned)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Filter             │ (Posts para próximas 2 horas)
└──────────┬──────────┘
           │
           ├─── No posts ───┐
           │                 │
           │                 ▼
           │        ┌─────────────────┐
           │        │  End            │
           │        └─────────────────┘
           │
           └─── Has posts ──┐
                            │
                            ▼
                   ┌─────────────────────┐
                   │  Loop Posts         │
                   │  For each post:     │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Format Reminder    │
                   │  (With hook, CTA)   │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  Evolution API      │
                   │  Send WhatsApp      │
                   └─────────────────────┘

// Mesmo workflow roda às 17:30 para posts 18h-20h
```

---

## 3. FLUXOS DE DADOS

### 3.1 Fluxo de Atualização de Métricas

```
┌────────────┐
│   Gerente  │
└─────┬──────┘
      │ 1. Exporta CSV do Meta Ads
      │
      ▼
┌──────────────────┐
│  Arquivo CSV     │
└─────┬────────────┘
      │ 2. Envia POST para webhook
      │
      ▼
┌──────────────────────────────────┐
│  n8n Workflow 1                  │
│  - Parse CSV                     │
│  - Validate                      │
│  - Calculate                     │
└─────┬────────────────────────────┘
      │ 3. POST /api/webhook/metrics
      │
      ▼
┌──────────────────────────────────┐
│  Backend API                     │
│  - Authenticate webhook token    │
│  - Validate data                 │
│  - Insert into DB                │
└─────┬────────────────────────────┘
      │ 4. Data saved
      │
      ▼
┌──────────────────────────────────┐
│  PostgreSQL                      │
│  - metrics table updated         │
└─────┬────────────────────────────┘
      │ 5. Dashboard refreshes
      │
      ▼
┌──────────────────────────────────┐
│  Frontend Dashboard              │
│  - GET /api/metrics              │
│  - Update charts                 │
└──────────────────────────────────┘
```

### 3.2 Fluxo de Alerta Automático

```
┌──────────────────────────────────┐
│  n8n Cron (18:00)                │
└─────┬────────────────────────────┘
      │ 1. Trigger
      │
      ▼
┌──────────────────────────────────┐
│  GET /api/metrics?date=today     │
└─────┬────────────────────────────┘
      │ 2. Return metrics
      │
      ▼
┌──────────────────────────────────┐
│  n8n Function Node               │
│  Check: CTR < 1.5%? YES!         │
└─────┬────────────────────────────┘
      │ 3. Alert needed
      │
      ▼
┌──────────────────────────────────┐
│  Format WhatsApp Message         │
│  "⚠️ CTR baixo: 1.2%"           │
└─────┬────────────────────────────┘
      │ 4. Formatted message
      │
      ▼
┌──────────────────────────────────┐
│  Evolution API                   │
│  POST /message/sendText          │
└─────┬────────────────────────────┘
      │ 5. Message sent
      │
      ▼
┌──────────────────────────────────┐
│  WhatsApp (Sabrina/Gerente)      │
│  🔔 Notificação recebida         │
└──────────────────────────────────┘
      │
      │ 6. Log alert
      ▼
┌──────────────────────────────────┐
│  POST /api/alerts                │
│  Save alert record               │
└──────────────────────────────────┘
```

### 3.3 Fluxo de Login

```
┌────────────┐
│  Usuário   │
└─────┬──────┘
      │ 1. Preenche email + senha
      │
      ▼
┌──────────────────────────────────┐
│  Frontend (index.html)           │
│  auth.js → axios.post()          │
└─────┬────────────────────────────┘
      │ 2. POST /api/auth/login
      │    { email, password }
      │
      ▼
┌──────────────────────────────────┐
│  Backend (/api/auth/login)       │
│  1. Find user by email           │
│  2. Compare password hash        │
│  3. Generate JWT                 │
└─────┬────────────────────────────┘
      │ 3. Return { token, user }
      │
      ▼
┌──────────────────────────────────┐
│  Frontend (auth.js)              │
│  1. Save token → localStorage    │
│  2. Save user → localStorage     │
│  3. Redirect → dashboard.html    │
└──────────────────────────────────┘
```

---

## 4. DECISÕES DE ARQUITETURA

### 4.1 Por que Vercel Serverless?
- ✅ Deploy simplificado (git push)
- ✅ Escala automática
- ✅ HTTPS automático
- ✅ Edge CDN global
- ✅ Zero configuração de infraestrutura
- ❌ Limitação: Cold starts (mitigado com keep-alive)

### 4.2 Por que PostgreSQL?
- ✅ Relacional (structured data)
- ✅ ACID compliance
- ✅ Queries complexas eficientes
- ✅ Suporte a JSONB (flexibilidade)
- ✅ Maduro e confiável
- ❌ Alternativa considerada: MongoDB (rejeitada por falta de necessidade de NoSQL)

### 4.3 Por que Alpine.js ao invés de React/Vue?
- ✅ Extremamente leve (15kb)
- ✅ Sintaxe declarativa simples
- ✅ Sem build step necessário
- ✅ Perfeito para projetos pequenos/médios
- ✅ Curva de aprendizado mínima
- ❌ Limitação: Não ideal para apps muito complexos (não é o caso)

### 4.4 Por que Chart.js?
- ✅ Simples e poderoso
- ✅ Gráficos bonitos out-of-the-box
- ✅ Responsivo
- ✅ Customizável
- ✅ Sem dependências pesadas

### 4.5 Por que n8n para automação?
- ✅ Já está instalado e configurado
- ✅ Interface visual (fácil manutenção)
- ✅ Integração nativa com centenas de serviços
- ✅ Self-hosted (controle total)
- ✅ Workflows versionáveis (JSON)

---

## 5. SEGURANÇA

### 5.1 Autenticação e Autorização

```
JWT Structure:
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "userId": "uuid",
    "email": "user@example.com",
    "role": "admin",
    "iat": 1234567890,
    "exp": 1234567890 + (7 * 24 * 60 * 60) // 7 dias
  },
  "signature": "..."
}
```

#### Proteção de Endpoints
```javascript
// Middleware de autenticação
function authenticateJWT(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'Token não fornecido' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(403).json({ error: 'Token inválido ou expirado' });
  }
}

// Aplicar em rotas protegidas
app.get('/api/metrics', authenticateJWT, getMetrics);
```

### 5.2 Proteção contra Ataques

#### SQL Injection
- ✅ Usar prepared statements (pg library)
- ✅ Validar e sanitizar inputs
- ✅ Nunca concatenar strings para queries

#### XSS (Cross-Site Scripting)
- ✅ Sanitizar output HTML
- ✅ Content Security Policy headers
- ✅ Usar textContent ao invés de innerHTML

#### CSRF (Cross-Site Request Forgery)
- ✅ Token CSRF em forms (se necessário)
- ✅ SameSite cookies
- ✅ Verificar origin header

#### Rate Limiting
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minuto
  max: 100, // 100 requests
  message: 'Muitas requisições, tente novamente em 1 minuto'
});

app.use('/api/', limiter);
```

### 5.3 Variáveis de Ambiente

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET=super_secret_key_change_in_production
JWT_EXPIRES_IN=7d
WEBHOOK_SECRET=webhook_secret_token
CORS_ORIGIN=https://dashboard-sabrina.vercel.app
NODE_ENV=production

# n8n (já configurado)
N8N_API_URL=https://fluxos.macspark.dev
N8N_API_KEY=your_n8n_api_key

# Evolution API
EVOLUTION_API_URL=https://evolution-api.example.com
EVOLUTION_API_KEY=your_evolution_key
WHATSAPP_NUMBER=+5511999999999
```

---

## 6. PERFORMANCE

### 6.1 Otimizações Frontend
- ✅ Minificação de CSS/JS
- ✅ Lazy loading de imagens
- ✅ Cache de assets estáticos (Vercel CDN)
- ✅ Debounce em buscas
- ✅ Virtual scrolling em listas longas (se necessário)

### 6.2 Otimizações Backend
- ✅ Connection pooling (PostgreSQL)
- ✅ Índices em colunas frequentemente consultadas
- ✅ Cache de queries repetitivas (Redis opcional)
- ✅ Pagination em listagens

### 6.3 Otimizações n8n
- ✅ Workflows desacoplados (não em cadeia)
- ✅ Timeout configurado (30s)
- ✅ Retry com backoff exponencial
- ✅ Logs estruturados para debug

---

## 7. MONITORAMENTO E LOGS

### 7.1 Logs de Aplicação
```javascript
// Estrutura de log
{
  "timestamp": "2025-10-20T18:00:00Z",
  "level": "info", // info, warn, error
  "service": "api", // api, n8n, evolution
  "action": "login",
  "userId": "uuid",
  "metadata": {
    "ip": "192.168.1.1",
    "userAgent": "..."
  },
  "message": "Usuário logado com sucesso"
}
```

### 7.2 Métricas a Monitorar
- API response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Database query time
- n8n workflow execution time
- Evolution API success rate
- WhatsApp delivery rate

### 7.3 Alertas Operacionais
- API down por > 5 minutos
- Database connection errors
- n8n workflow failures
- Evolution API errors > 10% nas últimas 24h
- Disk space > 80%

---

## 8. ESCALABILIDADE

### Cenário Atual (MVP)
- 1-5 usuários simultâneos
- ~100 requisições/dia
- 1 workflow execution a cada hora
- Database: < 1GB

### Crescimento Previsto (6 meses)
- 10-50 usuários
- ~1000 requisições/dia
- 10 workflows/hora
- Database: ~5GB

### Estratégias de Escala
1. **Horizontal** (se necessário):
   - Múltiplas instâncias Vercel (automático)
   - Read replicas PostgreSQL
   - Load balancer (Vercel cuida)

2. **Vertical** (primeiro passo):
   - Upgrade plan Vercel
   - Upgrade database tier
   - Otimizar queries

3. **Cache**:
   - Redis para dados frequentes
   - CDN para assets estáticos (já tem)
   - Browser cache headers

---

**Documento vivo**: Esta arquitetura será atualizada conforme evolução do sistema.

