# Setup Supabase - Data Warehouse Gratuito

**Versão:** 1.0.0  
**Data:** 18 de Outubro, 2025  
**Tempo Estimado:** 10-15 minutos

---

## 🎯 Objetivo

Configurar **Supabase** como data warehouse central gratuito para armazenar métricas de todas as fontes de marketing (Meta Ads, Google Analytics, Google Ads, YouTube).

**Vantagens:**
- ✅ **100% Gratuito** (Free tier: 500MB database, 2GB bandwidth)
- ✅ **PostgreSQL completo** com API REST automática
- ✅ **Integração nativa** com n8n
- ✅ **Dashboard embutido** para queries SQL
- ✅ **Real-time** (opcional para futuras features)

---

## 📋 Passo a Passo

### 1️⃣ **Criar Conta Supabase** (2 min)

1. Acesse: https://supabase.com
2. Clique em **"Start your project"**
3. Faça login com GitHub ou Email
4. ✅ Conta criada!

---

### 2️⃣ **Criar Novo Projeto** (3 min)

1. No dashboard, clique em **"New Project"**
2. Preencha:
   - **Name:** `marketing-metrics-sabrina`
   - **Database Password:** Escolha uma senha forte (salve!)
   - **Region:** `South America (São Paulo)` (mais próximo)
   - **Plan:** Free (já selecionado)
3. Clique em **"Create new project"**
4. ⏳ Aguarde 1-2 minutos (provisionamento)

---

### 3️⃣ **Obter Credenciais** (1 min)

1. No projeto criado, vá em **Settings** (menu lateral)
2. Clique em **API**
3. ✅ Copie e salve:
   - **Project URL:** `https://[seu-projeto].supabase.co`
   - **anon public key:** `eyJhbGc...` (token público)
   - **service_role key:** `eyJhbGc...` (token admin - CUIDADO!)

**⚠️ IMPORTANTE:** Salve no `.env` local (nunca comitar)

---

### 4️⃣ **Criar Database Schema** (5 min)

#### **Método 1: SQL Editor (Recomendado)**

1. No menu lateral, clique em **SQL Editor**
2. Clique em **"New Query"**
3. Cole o SQL abaixo:

```sql
-- Criar tabela de métricas diárias
CREATE TABLE IF NOT EXISTS daily_metrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Identificação
    data DATE NOT NULL,
    source VARCHAR(50) NOT NULL, -- 'meta_ads', 'google_analytics', 'google_ads', 'youtube', 'instagram'
    
    -- Métricas de Investimento
    spend DECIMAL(10,2) DEFAULT 0,
    budget DECIMAL(10,2) DEFAULT 0,
    
    -- Métricas de Alcance
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    frequency DECIMAL(5,2) DEFAULT 0,
    
    -- Métricas de Engajamento
    clicks INTEGER DEFAULT 0,
    ctr DECIMAL(5,2) DEFAULT 0,
    cpc DECIMAL(10,2) DEFAULT 0,
    cpe DECIMAL(10,2) DEFAULT 0,
    cpm DECIMAL(10,2) DEFAULT 0,
    
    -- Métricas de Conversão
    conversions INTEGER DEFAULT 0,
    cost_per_conversion DECIMAL(10,2) DEFAULT 0,
    new_followers INTEGER DEFAULT 0,
    cost_per_follower DECIMAL(10,2) DEFAULT 0,
    
    -- Métricas Específicas de Fonte
    sessions INTEGER DEFAULT 0,          -- Google Analytics
    users INTEGER DEFAULT 0,             -- Google Analytics
    bounce_rate DECIMAL(5,2) DEFAULT 0,  -- Google Analytics
    views INTEGER DEFAULT 0,             -- YouTube
    watch_time INTEGER DEFAULT 0,        -- YouTube (segundos)
    subscribers_gained INTEGER DEFAULT 0,-- YouTube
    
    -- Metadata
    notes TEXT,
    raw_data JSONB, -- Dados brutos completos da API
    
    -- Índices para performance
    UNIQUE(data, source)
);

-- Criar índices para queries rápidas
CREATE INDEX idx_daily_metrics_date ON daily_metrics(data DESC);
CREATE INDEX idx_daily_metrics_source ON daily_metrics(source);
CREATE INDEX idx_daily_metrics_date_source ON daily_metrics(data DESC, source);

-- Criar view consolidada (todas fontes)
CREATE OR REPLACE VIEW metrics_consolidated AS
SELECT 
    data,
    SUM(spend) as total_spend,
    SUM(reach) as total_reach,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    AVG(ctr) as avg_ctr,
    AVG(cpc) as avg_cpc,
    SUM(new_followers) as total_new_followers,
    AVG(cost_per_follower) as avg_cost_per_follower,
    SUM(sessions) as total_sessions,
    SUM(users) as total_users,
    SUM(views) as total_views
FROM daily_metrics
GROUP BY data
ORDER BY data DESC;

-- Criar view de performance por fonte
CREATE OR REPLACE VIEW performance_by_source AS
SELECT 
    source,
    COUNT(*) as days_tracked,
    SUM(spend) as total_spend,
    SUM(new_followers) as total_followers,
    AVG(cost_per_follower) as avg_cost_per_follower,
    AVG(ctr) as avg_ctr,
    SUM(views) as total_views
FROM daily_metrics
GROUP BY source
ORDER BY total_spend DESC;

-- Comentários nas tabelas
COMMENT ON TABLE daily_metrics IS 'Métricas diárias agregadas de todas as fontes de marketing';
COMMENT ON COLUMN daily_metrics.source IS 'Fonte dos dados: meta_ads, google_analytics, google_ads, youtube, instagram';
COMMENT ON COLUMN daily_metrics.raw_data IS 'JSON com dados brutos completos da API para auditoria';
```

4. Clique em **"Run"** (Ctrl/Cmd + Enter)
5. ✅ Tabela criada com sucesso!

#### **Método 2: Table Editor (Visual)**

Se preferir interface visual:

1. Menu lateral → **Table Editor**
2. **"Create a new table"**
3. Nome: `daily_metrics`
4. Adicionar colunas conforme SQL acima
5. ✅ Salvar

---

### 5️⃣ **Configurar Row Level Security (Opcional)** (2 min)

Por segurança, configure políticas de acesso:

```sql
-- Habilitar RLS
ALTER TABLE daily_metrics ENABLE ROW LEVEL SECURITY;

-- Política: Service role pode tudo
CREATE POLICY "Service role full access"
ON daily_metrics
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Política: Anon key apenas leitura
CREATE POLICY "Anon read only"
ON daily_metrics
FOR SELECT
TO anon
USING (true);
```

---

### 6️⃣ **Testar Conexão** (2 min)

#### **Via SQL Editor:**

```sql
-- Inserir teste
INSERT INTO daily_metrics (data, source, spend, reach, new_followers, notes)
VALUES (CURRENT_DATE, 'test', 10.50, 1000, 5, 'Teste de conexão');

-- Verificar
SELECT * FROM daily_metrics ORDER BY created_at DESC LIMIT 5;

-- Limpar teste
DELETE FROM daily_metrics WHERE source = 'test';
```

✅ Se retornou dados, conexão OK!

---

### 7️⃣ **Configurar no `.env`** (2 min)

Adicione ao seu arquivo `.env` local:

```bash
# Supabase Configuration
SUPABASE_URL=https://[seu-projeto].supabase.co
SUPABASE_ANON_KEY=eyJhbGc...  # anon public key
SUPABASE_SERVICE_KEY=eyJhbGc... # service_role key (CUIDADO!)

# Database Connection (para Python/n8n)
SUPABASE_DB_HOST=[seu-projeto].supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=[sua-senha]
```

⚠️ **NUNCA commitar** `.env` no Git!

---

## 🔗 Integrações

### **n8n (HTTP Request Node)**

```json
{
  "method": "POST",
  "url": "={{$env.SUPABASE_URL}}/rest/v1/daily_metrics",
  "headers": {
    "apikey": "={{$env.SUPABASE_ANON_KEY}}",
    "Authorization": "Bearer ={{$env.SUPABASE_ANON_KEY}}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
  },
  "body": {
    "data": "2025-10-18",
    "source": "meta_ads",
    "spend": 40.0,
    "reach": 15234,
    "ctr": 0.42,
    "new_followers": 12
  }
}
```

### **Python (supabase-py)**

```python
from supabase import create_client, Client

supabase: Client = create_client(
    supabase_url=os.getenv('SUPABASE_URL'),
    supabase_key=os.getenv('SUPABASE_SERVICE_KEY')
)

# Inserir métrica
data = supabase.table('daily_metrics').insert({
    "data": "2025-10-18",
    "source": "meta_ads",
    "spend": 40.0,
    "reach": 15234,
    "new_followers": 12
}).execute()

# Query métricas
metrics = supabase.table('daily_metrics')\
    .select("*")\
    .eq("source", "meta_ads")\
    .order("data", desc=True)\
    .limit(30)\
    .execute()
```

---

## 📊 Queries Úteis

### **Métricas Consolidadas (Últimos 7 dias)**

```sql
SELECT * FROM metrics_consolidated
WHERE data >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY data DESC;
```

### **Performance por Fonte**

```sql
SELECT * FROM performance_by_source;
```

### **Custo por Seguidor Médio (Mensal)**

```sql
SELECT 
    DATE_TRUNC('month', data) as month,
    source,
    SUM(spend) as total_spend,
    SUM(new_followers) as total_followers,
    CASE 
        WHEN SUM(new_followers) > 0 
        THEN SUM(spend) / SUM(new_followers) 
        ELSE 0 
    END as cost_per_follower
FROM daily_metrics
WHERE new_followers IS NOT NULL
GROUP BY DATE_TRUNC('month', data), source
ORDER BY month DESC, source;
```

---

## 🛠️ Troubleshooting

### **Erro: "relation does not exist"**
- Solução: Re-executar o SQL de criação de tabela

### **Erro: "JWT expired"**
- Solução: Renovar anon key no dashboard Supabase (Settings → API)

### **Erro: "permission denied"**
- Solução: Usar `SUPABASE_SERVICE_KEY` para operações de escrita

### **Slow Queries**
- Solução: Verificar índices com `EXPLAIN ANALYZE SELECT ...`

---

## 📚 Recursos

- **Dashboard:** https://supabase.com/dashboard/project/[seu-projeto]
- **Docs Oficiais:** https://supabase.com/docs
- **SQL Editor:** Aba "SQL Editor" no dashboard
- **Table Editor:** Aba "Table Editor" para visualização
- **API Docs:** Aba "API" para ver endpoints REST gerados

---

## 🔐 Segurança

✅ **Implementado:**
- RLS (Row Level Security) ativado
- Anon key apenas leitura
- Service key para escrita (protegido em .env)

⚠️ **Recomendações:**
- Nunca expor `service_role key` em frontend
- Usar `.env` local (gitignored)
- Rotacionar keys a cada 6 meses

---

## ✅ Checklist de Setup

- [ ] Conta Supabase criada
- [ ] Projeto `marketing-metrics-sabrina` criado
- [ ] Tabela `daily_metrics` criada via SQL
- [ ] Views `metrics_consolidated` e `performance_by_source` criadas
- [ ] Credenciais copiadas (URL + anon key + service key)
- [ ] `.env` atualizado com variáveis Supabase
- [ ] Teste de inserção executado com sucesso
- [ ] RLS configurado (opcional mas recomendado)

---

**🎉 Supabase configurado! Próximo: Criar workflows n8n**

**Próximo guia:** `docs/setup-apache-superset.md`

