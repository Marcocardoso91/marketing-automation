# 🏗️ BLUEPRINT DE ARQUITETURA
## Facebook Ads AI Agent - Diagrama Técnico Completo

---

## 📐 VISÃO GERAL DA ARQUITETURA

### Camadas e Componentes

```mermaid
graph TB
    subgraph "CAMADA 1: EDGE & PROXY"
        TRAEFIK[🔀 Traefik v2.10<br/>- SSL/TLS Automático<br/>- Load Balancer<br/>- Rate Limiting]
    end
    
    subgraph "CAMADA 2: APPLICATION"
        FASTAPI[⚡ FastAPI<br/>main.py<br/>Port 8000]
        
        subgraph "Modules"
            AGENTS[🤖 Agents<br/>facebook_agent.py]
            ANALYTICS[📊 Analytics<br/>performance_analyzer.py]
            AUTOMATION[⚙️ Automation<br/>campaign_optimizer.py]
            REPORTS[📋 Reports<br/>report_generator.py]
        end
        
        FASTAPI --> AGENTS
        FASTAPI --> ANALYTICS
        FASTAPI --> AUTOMATION
        FASTAPI --> REPORTS
    end
    
    subgraph "CAMADA 3: INTEGRATION"
        N8N[🔗 n8n Workflows<br/>Port 5678]
        
        subgraph "Workflows"
            WF1[fb_fetch_metrics<br/>30min interval]
            WF2[build_recommendations<br/>on demand]
            WF3[send_alerts_multi<br/>instant]
            WF4[calendar_context<br/>sync]
        end
        
        N8N --> WF1
        N8N --> WF2
        N8N --> WF3
        N8N --> WF4
    end
    
    subgraph "CAMADA 4: EXTERNAL APIs"
        FBAPI[📘 Facebook Marketing API<br/>graph.facebook.com]
        SLACK[💬 Slack<br/>hooks.slack.com]
        WHATSAPP[📱 WhatsApp Business<br/>via n8n]
        EMAIL[📧 SMTP<br/>SendGrid/SES]
        GCAL[📅 Google Calendar API<br/>calendar.google.com]
    end
    
    subgraph "CAMADA 5: DATA"
        POSTGRES[(🐘 PostgreSQL 15<br/>Port 5432<br/>- Campaigns<br/>- Insights<br/>- Users<br/>- Conversations)]
        REDIS[(🔴 Redis 7<br/>Port 6379<br/>- Cache<br/>- Celery Queue<br/>- Session Store)]
    end
    
    subgraph "CAMADA 6: WORKERS"
        CELERY[⚙️ Celery Workers<br/>Background Jobs]
        CELERYBEAT[⏰ Celery Beat<br/>Scheduler]
        FLOWER[🌸 Flower<br/>Port 5555<br/>Task Monitor]
        
        CELERYBEAT -.Schedule.-> CELERY
        CELERY -.Status.-> FLOWER
    end
    
    subgraph "CAMADA 7: OBSERVABILITY"
        PROM[📈 Prometheus<br/>Port 9090<br/>Metrics Collection]
        GRAFANA[📊 Grafana<br/>Port 3000<br/>Dashboards]
        
        PROM --> GRAFANA
    end
    
    %% Connections
    USER[👤 Usuário] --> TRAEFIK
    CURSOR[💻 Cursor IDE] --> TRAEFIK
    
    TRAEFIK --> FASTAPI
    TRAEFIK --> GRAFANA
    TRAEFIK --> N8N
    TRAEFIK --> FLOWER
    
    FASTAPI --> POSTGRES
    FASTAPI --> REDIS
    FASTAPI --> N8N
    FASTAPI --> PROM
    
    AGENTS --> FBAPI
    WF1 --> FBAPI
    WF3 --> SLACK
    WF3 --> WHATSAPP
    WF3 --> EMAIL
    WF4 --> GCAL
    
    CELERY --> REDIS
    CELERY --> POSTGRES
    CELERY --> N8N
    
    ANALYTICS --> POSTGRES
    AUTOMATION --> POSTGRES
    REPORTS --> POSTGRES
    
    style TRAEFIK fill:#ff9999,stroke:#333,stroke-width:4px
    style FASTAPI fill:#99ccff,stroke:#333,stroke-width:3px
    style N8N fill:#ffcc99,stroke:#333,stroke-width:3px
    style POSTGRES fill:#ddddff,stroke:#333,stroke-width:2px
    style REDIS fill:#ffdddd,stroke:#333,stroke-width:2px
    style PROM fill:#ffffdd,stroke:#333,stroke-width:2px
```

---

## 🔄 FLUXOS DE DADOS PRINCIPAIS

### Fluxo 1: Coleta Automática de Métricas (Job Agendado)

```mermaid
sequenceDiagram
    autonumber
    participant CB as Celery Beat
    participant CW as Celery Worker
    participant A as Facebook Agent
    participant FB as Facebook API
    participant DB as PostgreSQL
    participant R as Redis Cache
    participant PA as Performance Analyzer
    participant N as n8n
    
    Note over CB: A cada 30 minutos
    CB->>CW: Trigger task collect_metrics
    CW->>A: get_all_campaigns()
    A->>FB: GET /v18.0/act_{account}/campaigns
    FB-->>A: Lista de campanhas
    
    loop Para cada campanha
        A->>FB: GET /v18.0/{campaign_id}/insights
        FB-->>A: Métricas (CTR, CPA, ROAS)
        A->>DB: INSERT/UPDATE metrics
        A->>R: SET cache:campaign:{id}
    end
    
    CW->>PA: analyze_performance(metrics)
    PA->>PA: Calcular scores e detectar anomalias
    
    alt Problema detectado
        PA->>N: Webhook build_recommendations
        N->>N: Gerar sugestões
        N->>N: Trigger send_alerts_multi
        N-->>Slack: Enviar alerta
        N-->>Email: Enviar resumo
    end
    
    PA-->>CW: Análise completa
    CW-->>CB: Task completed ✓
```

### Fluxo 2: Usuário Consulta via API REST

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário
    participant T as Traefik
    participant F as FastAPI
    participant R as Redis Cache
    participant A as Facebook Agent
    participant FB as Facebook API
    participant DB as PostgreSQL
    participant P as Prometheus
    
    U->>T: GET /api/v1/campaigns?status=ACTIVE
    T->>F: Forward request
    F->>P: Incrementar api_requests_total
    
    F->>R: GET cache:campaigns:active
    
    alt Cache hit
        R-->>F: Campanhas do cache
        F-->>T: 200 OK + Data (cache)
    else Cache miss
        R-->>F: null
        F->>A: get_campaigns(status="ACTIVE")
        A->>FB: GET /campaigns?filtering=[{status:ACTIVE}]
        FB-->>A: Campanhas ativas
        A->>DB: Salvar histórico
        A->>R: SET cache:campaigns:active (TTL 5min)
        A-->>F: Campanhas
        F-->>T: 200 OK + Data (fresh)
    end
    
    T-->>U: Resposta JSON
    F->>P: Histogram request_duration
```

### Fluxo 3: Chat Conversacional com Contexto

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário/Cursor
    participant F as FastAPI
    participant CM as Context Memory
    participant A as Facebook Agent
    participant FB as Facebook API
    participant NLP as LangChain NLP
    participant DB as PostgreSQL
    
    U->>F: POST /api/v1/chat<br/>{"message": "CTR das campanhas?"}
    
    F->>CM: get_conversation_history(user_id)
    CM->>DB: SELECT * FROM conversation_memory<br/>WHERE user_id = ? LIMIT 10
    DB-->>CM: Últimas 10 interações
    CM-->>F: Contexto histórico
    
    F->>NLP: Processar query + contexto
    NLP->>NLP: Entender intenção:<br/>"Buscar CTR de campanhas ativas"
    NLP-->>F: Intent: QUERY_METRICS, entity: CTR
    
    F->>A: get_campaigns_with_insights()
    A->>FB: Buscar métricas
    FB-->>A: Dados
    A-->>F: Campanhas + CTR
    
    F->>NLP: Gerar resposta natural
    NLP-->>F: "As campanhas ativas têm CTR médio de 2.5%.<br/>Campanha X está com 4.2% (excelente)..."
    
    F->>CM: add_message(user_id, role="user", message)
    F->>CM: add_message(user_id, role="assistant", message)
    CM->>DB: INSERT INTO conversation_memory
    
    F-->>U: Resposta formatada
```

### Fluxo 4: Automação - Pausa por Performance Ruim

```mermaid
sequenceDiagram
    autonumber
    participant CW as Celery Worker
    participant A as Facebook Agent
    participant FB as Facebook API
    participant CO as Campaign Optimizer
    participant DB as PostgreSQL
    participant N as n8n
    participant S as Slack
    
    Note over CW: Job monitor_performance
    CW->>A: get_campaigns_insights()
    A->>FB: GET insights last_3d
    FB-->>A: Métricas recentes
    
    A->>CO: evaluate_campaigns(insights)
    
    loop Para cada campanha
        alt CTR < 1% OU CPA > 50
            CO->>CO: Flag para pausa
            CO->>DB: INSERT INTO audit_log<br/>(action: PAUSE_SUGGESTED)
            
            CO->>N: Webhook send_alert<br/>{campaign, issue, metrics}
            N->>S: POST Slack<br/>"⚠️ Campanha {name}<br/>CTR: 0.8% (alvo: >1%)"
            S-->>N: 200 OK
            
            Note over CO: Modo sugestão (não pausa automática)
            CO->>DB: INSERT INTO suggestions<br/>(type: PAUSE, reason, campaign_id)
        end
    end
    
    CO-->>CW: Análise concluída + sugestões
    CW->>DB: UPDATE job_history SET status='completed'
```

---

## 📦 ESTRUTURA DE MÓDULOS DETALHADA

### Estrutura de Diretórios Completa

```
facebook-ads-ai-agent/
│
├── 📁 src/                          # Código fonte principal
│   │
│   ├── 📁 agents/                   # Agentes inteligentes
│   │   ├── __init__.py
│   │   ├── facebook_agent.py        # Agente principal Facebook Ads
│   │   ├── base_agent.py            # Classe base abstrata
│   │   └── agent_factory.py         # Factory pattern para agentes
│   │
│   ├── 📁 api/                      # APIs REST (FastAPI Routers)
│   │   ├── __init__.py
│   │   ├── campaigns.py             # CRUD de campanhas
│   │   ├── analytics.py             # Endpoints de análise
│   │   ├── automation.py            # Automações e otimizações
│   │   ├── chat.py                  # Interface conversacional
│   │   ├── reports.py               # Geração de relatórios
│   │   └── webhooks.py              # Webhooks n8n
│   │
│   ├── 📁 analytics/                # Módulos de análise
│   │   ├── __init__.py
│   │   ├── performance_analyzer.py  # Análise de performance
│   │   ├── anomaly_detector.py      # Detecção de anomalias (ML)
│   │   ├── trend_analyzer.py        # Análise de tendências
│   │   └── scoring_engine.py        # Engine de pontuação
│   │
│   ├── 📁 automation/               # Automações e otimizações
│   │   ├── __init__.py
│   │   ├── campaign_optimizer.py    # Otimização de campanhas
│   │   ├── budget_allocator.py      # Alocação inteligente de budget
│   │   ├── pause_manager.py         # Gerenciamento de pausas
│   │   └── scaling_advisor.py       # Advisor de escalonamento
│   │
│   ├── 📁 reports/                  # Geração de relatórios
│   │   ├── __init__.py
│   │   ├── report_generator.py      # Gerador principal
│   │   ├── templates/               # Templates de relatórios
│   │   │   ├── daily_report.html
│   │   │   ├── weekly_summary.html
│   │   │   └── executive_report.html
│   │   └── exporters/               # Exportadores
│   │       ├── pdf_exporter.py
│   │       ├── excel_exporter.py
│   │       └── csv_exporter.py
│   │
│   ├── 📁 integrations/             # Integrações externas
│   │   ├── __init__.py
│   │   ├── n8n_client.py            # Cliente n8n
│   │   ├── facebook_client.py       # Cliente Facebook API
│   │   ├── slack_client.py          # Cliente Slack
│   │   ├── whatsapp_client.py       # Cliente WhatsApp
│   │   └── calendar_client.py       # Cliente Google Calendar
│   │
│   ├── 📁 models/                   # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── campaign.py              # Modelo Campaign
│   │   ├── insight.py               # Modelo Insight
│   │   ├── user.py                  # Modelo User
│   │   ├── conversation.py          # Modelo ConversationMemory
│   │   ├── suggestion.py            # Modelo Suggestion
│   │   └── audit_log.py             # Modelo AuditLog
│   │
│   ├── 📁 schemas/                  # Pydantic Schemas
│   │   ├── __init__.py
│   │   ├── campaign_schemas.py
│   │   ├── insight_schemas.py
│   │   ├── chat_schemas.py
│   │   └── report_schemas.py
│   │
│   ├── 📁 tasks/                    # Tarefas Celery
│   │   ├── __init__.py
│   │   ├── celery_app.py            # Configuração Celery
│   │   ├── collectors.py            # Coletores de métricas
│   │   ├── processors.py            # Processadores de dados
│   │   ├── notifiers.py             # Notificadores (alertas)
│   │   └── schedulers.py            # Agendadores
│   │
│   └── 📁 utils/                    # Utilitários
│       ├── __init__.py
│       ├── config.py                # Configurações (Pydantic Settings)
│       ├── database.py              # Setup SQLAlchemy
│       ├── logger.py                # Logger estruturado
│       ├── api_client.py            # Cliente com rate limiting
│       ├── token_manager.py         # Gerenciador de tokens
│       ├── context_memory.py        # Memória de contexto
│       ├── metrics.py               # Métricas Prometheus
│       ├── cache.py                 # Cache Redis
│       └── validators.py            # Validadores customizados
│
├── 📁 tests/                        # Testes automatizados
│   ├── conftest.py                  # Fixtures compartilhadas
│   ├── 📁 unit/                     # Testes unitários
│   │   ├── test_facebook_agent.py
│   │   ├── test_performance_analyzer.py
│   │   ├── test_campaign_optimizer.py
│   │   └── test_report_generator.py
│   ├── 📁 integration/              # Testes de integração
│   │   ├── test_api_endpoints.py
│   │   ├── test_facebook_api.py
│   │   ├── test_n8n_webhooks.py
│   │   └── test_database.py
│   ├── 📁 e2e/                      # Testes end-to-end
│   │   ├── test_full_flow.py
│   │   └── test_automation_flow.py
│   └── 📁 features/                 # BDD/Gherkin
│       ├── account_disabled.feature
│       ├── performance_alert.feature
│       └── budget_optimization.feature
│
├── 📁 alembic/                      # Migrações de banco
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_suggestions.py
│       └── 003_add_audit_log.py
│
├── 📁 config/                       # Arquivos de configuração
│   ├── prometheus.yml               # Config Prometheus
│   ├── grafana/
│   │   ├── datasources.yml
│   │   └── dashboards/
│   │       ├── system_health.json
│   │       ├── facebook_ads.json
│   │       └── agent_activity.json
│   └── n8n/
│       ├── workflows/
│       │   ├── fb_fetch_metrics.json
│       │   ├── send_alerts_multi.json
│       │   └── calendar_context.json
│       └── credentials.json.example
│
├── 📁 scripts/                      # Scripts utilitários
│   ├── deploy.sh                    # Script de deploy
│   ├── backup.sh                    # Script de backup
│   ├── seed_database.py             # Popular banco com dados teste
│   └── migrate_data.py              # Migração de dados
│
├── 📁 docs/                         # Documentação
│   └── prd/facebook-ads-agent/
│       ├── PRD.en-US.md
│       ├── decisions.md
│       ├── backlog.csv
│       ├── coerencia.md
│       └── system-map.md
│
├── 📁 logs/                         # Logs da aplicação
│   ├── app.log
│   ├── celery.log
│   └── error.log
│
├── 📁 data/                         # Dados e cache
│   ├── cache/                       # Cache local
│   └── exports/                     # Relatórios exportados
│
├── main.py                          # Ponto de entrada FastAPI
├── requirements.txt                 # Dependências Python
├── requirements-dev.txt             # Dependências desenvolvimento
├── Dockerfile                       # Container aplicação
├── docker-compose.yml               # Orquestração dev
├── docker-compose.prod.yml          # Orquestração produção
├── .env.example                     # Template variáveis ambiente
├── .gitignore                       # Git ignore
├── pytest.ini                       # Config pytest
├── Makefile                         # Comandos utilitários
├── ci-cd.yml                        # Pipeline GitHub Actions
├── locustfile.py                    # Testes de carga
├── alembic.ini                      # Config Alembic
└── README.md                        # Documentação principal
```

---

## 🗄️ MODELO DE DADOS (Entidades Principais)

### Schema PostgreSQL

```mermaid
erDiagram
    USERS ||--o{ CONVERSATIONS : has
    USERS {
        uuid id PK
        string email UK
        string name
        jsonb preferences
        timestamp created_at
        timestamp updated_at
    }
    
    CAMPAIGNS ||--o{ INSIGHTS : generates
    CAMPAIGNS {
        string id PK "Facebook Campaign ID"
        string name
        string status
        string objective
        decimal daily_budget
        decimal lifetime_budget
        timestamp created_time
        timestamp updated_time
        timestamp synced_at
    }
    
    INSIGHTS {
        uuid id PK
        string campaign_id FK
        date date
        integer impressions
        integer clicks
        decimal spend
        decimal ctr
        decimal cpc
        decimal cpm
        decimal cpa
        decimal roas
        timestamp collected_at
    }
    
    SUGGESTIONS ||--o{ CAMPAIGNS : recommends
    SUGGESTIONS {
        uuid id PK
        string campaign_id FK
        string type "PAUSE|BUDGET_UP|BUDGET_DOWN"
        string reason
        jsonb data
        string status "PENDING|ACCEPTED|REJECTED"
        timestamp created_at
    }
    
    CONVERSATIONS {
        uuid id PK
        uuid user_id FK
        string session_id
        string role "user|assistant"
        text message
        jsonb metadata
        timestamp timestamp
    }
    
    AUDIT_LOG {
        uuid id PK
        string action
        string entity_type
        string entity_id
        jsonb before_state
        jsonb after_state
        string user_id
        timestamp timestamp
    }
```

---

## 🔐 SEGURANÇA E CONFORMIDADE

### Camadas de Segurança

```mermaid
graph LR
    subgraph "Perímetro"
        WAF[🛡️ WAF/Firewall]
        TRAEFIK[🔀 Traefik<br/>SSL/TLS]
    end
    
    subgraph "Autenticação"
        JWT[🔑 JWT Tokens]
        OAUTH[📱 OAuth 2.0]
    end
    
    subgraph "Autorização"
        RBAC[👥 RBAC<br/>Role Based Access]
        API_KEY[🔐 API Keys]
    end
    
    subgraph "Dados"
        ENCRYPT[🔒 Encryption at Rest]
        MASK[🙈 Data Masking]
        AUDIT[📝 Audit Logs]
    end
    
    subgraph "Network"
        VPN[🔒 VPN]
        IPSEC[🔐 IPSec]
    end
    
    WAF --> TRAEFIK
    TRAEFIK --> JWT
    TRAEFIK --> OAUTH
    JWT --> RBAC
    OAUTH --> RBAC
    RBAC --> API_KEY
    API_KEY --> ENCRYPT
    ENCRYPT --> MASK
    MASK --> AUDIT
    
    style WAF fill:#ff9999
    style TRAEFIK fill:#ff9999
    style JWT fill:#99ccff
    style OAUTH fill:#99ccff
    style RBAC fill:#99ff99
    style ENCRYPT fill:#ffcc99
```

### Conformidade LGPD

| Requisito | Implementação | Status |
|-----------|---------------|--------|
| Consentimento | Termo de aceite na criação de usuário | ✅ |
| Anonimização | Hash de dados sensíveis, sem PII desnecessário | ✅ |
| Direito ao Esquecimento | Endpoint DELETE /api/v1/users/{id}/data | 🟡 |
| Portabilidade | Endpoint GET /api/v1/users/{id}/export | 🟡 |
| Auditoria | Tabela audit_log com histórico completo | ✅ |
| Segurança | Criptografia em repouso e trânsito | ✅ |
| DPO | Contato data-protection@company.com | 🟡 |

---

## 📊 OBSERVABILIDADE - STACK COMPLETA

### Métricas Prometheus

```yaml
# Métricas customizadas da aplicação

# Counters (eventos que só aumentam)
- api_requests_total{method, endpoint, status}
- facebook_api_calls_total{method, status}
- alerts_sent_total{channel, severity}
- suggestions_generated_total{type}
- campaigns_analyzed_total

# Histograms (distribuição de valores)
- request_duration_seconds{method, endpoint}
- facebook_api_latency_seconds{method}
- database_query_duration_seconds{table}
- celery_task_duration_seconds{task_name}

# Gauges (valores instantâneos)
- active_campaigns_count
- daily_spend_usd
- active_users_count
- redis_memory_usage_bytes
- postgres_connections_active

# Summaries
- campaign_ctr_distribution
- campaign_cpa_distribution
```

### Dashboards Grafana

#### Dashboard 1: System Health
- CPU, RAM, Disk usage
- Network I/O
- Container health
- Error rates

#### Dashboard 2: Facebook Ads Performance
- Spend vs Budget
- CTR trends
- CPA trends
- ROAS trends
- Campaign count by status

#### Dashboard 3: Agent Activity
- Suggestions generated/hour
- Alerts sent/hour
- Automations executed
- Chat interactions

#### Dashboard 4: API Metrics
- Requests/second
- Latency P50/P95/P99
- Error rate 4xx/5xx
- Top endpoints

---

## 🚀 DEPLOY E ESCALABILIDADE

### Estratégia de Deploy

```mermaid
graph LR
    subgraph "Desenvolvimento"
        DEV[💻 Local Docker Compose]
    end
    
    subgraph "Staging"
        STAGE[🧪 VPS Staging<br/>staging.fbads.com]
    end
    
    subgraph "Produção"
        PROD[🚀 VPS Produção<br/>fbads.com]
    end
    
    subgraph "CI/CD"
        GIT[📦 Git Push]
        CI[⚙️ GitHub Actions]
        BUILD[🏗️ Docker Build]
        TEST[🧪 Tests]
        DEPLOY[🚀 Deploy SSH]
    end
    
    DEV -->|commit| GIT
    GIT --> CI
    CI --> TEST
    TEST --> BUILD
    BUILD -->|auto| STAGE
    STAGE -->|manual approval| DEPLOY
    DEPLOY --> PROD
    
    style PROD fill:#99ff99,stroke:#333,stroke-width:3px
```

### Escalabilidade Horizontal

| Componente | Limite Atual | Escala até | Como Escalar |
|------------|--------------|------------|--------------|
| FastAPI | 1 instância | 10+ | Adicionar replicas no docker-compose, load balancer Traefik |
| Celery Workers | 1 worker | 20+ | Aumentar replicas, usar Kubernetes |
| PostgreSQL | 1 instância | Read replicas | Master-Slave replication, PgPool |
| Redis | 1 instância | Cluster | Redis Cluster mode (3+ nodes) |
| n8n | 1 instância | Queue mode | n8n Queue mode com múltiplos workers |

---

**Blueprint criado por:** AI Agent (Claude Sonnet 4.5)  
**Data:** 18 de Outubro de 2025  
**Versão:** 1.0.0


