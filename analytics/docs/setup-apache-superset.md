# Setup Apache Superset - Visualização de Dados

**Versão:** 1.0.0  
**Data:** 18 de Outubro, 2025  
**Tempo Estimado:** 20-30 minutos

---

## 🎯 Objetivo

Configurar **Apache Superset** como plataforma gratuita de visualização e Business Intelligence para criar dashboards avançados com métricas de marketing.

**Vantagens:**
- ✅ **100% Gratuito** e open-source
- ✅ **40+ tipos de visualizações** (linha, barra, pizza, heatmap, etc)
- ✅ **SQL Lab** para queries customizadas
- ✅ **Alternativa ao Tableau/Power BI** sem custo
- ✅ **Self-hosted** (controle total)

---

## 📋 Passo a Passo

### 1️⃣ **Instalação via Docker** (5 min)

#### **Opção A: Docker Compose (Recomendado)**

1. Criar arquivo `docker-compose.superset.yml`:

```yaml
version: '3.8'

services:
  superset:
    image: apache/superset:latest
    container_name: superset
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=YOUR_SECRET_KEY_HERE_CHANGE_THIS
    volumes:
      - superset_home:/app/superset_home
    restart: unless-stopped
    command: >
      sh -c "
      superset db upgrade &&
      superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password admin &&
      superset init &&
      superset run -h 0.0.0.0 -p 8088 --with-threads --reload
      "

volumes:
  superset_home:
```

2. Executar:
```bash
docker-compose -f docker-compose.superset.yml up -d
```

3. Aguardar 1-2 minutos (inicialização)

4. Acessar: http://localhost:8088

5. Login:
   - **Username:** `admin`
   - **Password:** `admin` (⚠️ TROCAR DEPOIS!)

✅ **Superset rodando!**

---

#### **Opção B: Docker Run (Simples)**

```bash
docker run -d \
  --name superset \
  -p 8088:8088 \
  -e "SUPERSET_SECRET_KEY=YOUR_SECRET_KEY_HERE" \
  apache/superset:latest

# Inicializar database
docker exec -it superset superset db upgrade

# Criar admin
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin

# Carregar exemplos (opcional)
docker exec -it superset superset init

# Reiniciar
docker restart superset
```

---

### 2️⃣ **Conectar ao Supabase** (5 min)

1. **No Superset, vá em:**
   - Menu superior direito → **Settings** → **Database Connections**
   - Clique em **"+ Database"**

2. **Selecionar PostgreSQL:**
   - Escolha **"PostgreSQL"** da lista

3. **Preencher Credenciais:**

```
DISPLAY NAME: Supabase Marketing Metrics

SQLAlchemy URI:
postgresql://postgres:[SUA-SENHA]@db.[seu-projeto].supabase.co:5432/postgres
```

**Formato completo:**
```
postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
```

**Exemplo:**
```
postgresql://postgres:minha_senha_forte@db.abcd1234.supabase.co:5432/postgres
```

4. **Testar Conexão:**
   - Clique em **"Test Connection"**
   - ✅ Deve aparecer "Connection looks good!"

5. **Salvar:**
   - Clique em **"Connect"**

✅ **Supabase conectado ao Superset!**

---

### 3️⃣ **Criar Datasets** (5 min)

Datasets são "views" das tabelas que você quer visualizar.

1. **Menu superior:** **Data** → **Datasets**
2. Clique em **"+ Dataset"**
3. Preencher:
   - **Database:** `Supabase Marketing Metrics`
   - **Schema:** `public`
   - **Table:** `daily_metrics`
4. Clique em **"Create Dataset and Create Chart"**

Repetir para as views:
- `metrics_consolidated`
- `performance_by_source`

✅ **Datasets criados!**

---

### 4️⃣ **Criar Dashboards** (10-15 min)

#### **Dashboard 1: Overview Geral**

1. Menu **Dashboards** → **"+ Dashboard"**
2. Nome: `📊 Marketing Overview - Sabrina`
3. Adicionar Charts:

**Chart 1: Gasto Total por Dia (Linha)**
- Dataset: `daily_metrics`
- Chart Type: `Time-series Line Chart`
- Time Column: `data`
- Metrics: `SUM(spend)`
- Group by: `source`

**Chart 2: Novos Seguidores por Fonte (Barra)**
- Dataset: `performance_by_source`
- Chart Type: `Bar Chart`
- X-axis: `source`
- Metrics: `SUM(total_followers)`

**Chart 3: CTR Médio (Gauge)**
- Dataset: `metrics_consolidated`
- Chart Type: `Gauge Chart`
- Metric: `AVG(avg_ctr)`
- Min: 0, Max: 3, Target: 1.5

**Chart 4: Custo por Seguidor (KPI)**
- Dataset: `daily_metrics`
- Chart Type: `Big Number`
- Metric: `AVG(cost_per_follower)`

---

#### **Dashboard 2: Meta Ads Detalhado**

Filtro: `source = 'meta_ads'`

Charts:
1. **Gasto Diário** (Linha + Barra combinado)
2. **CTR vs Meta** (Linha com threshold)
3. **Frequência** (Linha + alerta se >2,5)
4. **Custo por Métrica** (Tabela: CPC, CPE, CPM)

---

#### **Dashboard 3: Google Ads**

Filtro: `source = 'google_ads'`

Charts:
1. **Impressões vs Cliques** (Linha dupla)
2. **CPC ao Longo do Tempo** (Linha)
3. **Taxa de Conversão** (Barra)
4. **ROI** (Big Number)

---

#### **Dashboard 4: YouTube Analytics**

Filtro: `source = 'youtube'`

Charts:
1. **Views Diárias** (Linha)
2. **Watch Time** (Área)
3. **Novos Inscritos** (Barra)
4. **Taxa de Retenção** (Percentual)

---

### 5️⃣ **Queries SQL Úteis** (Copiar no SQL Lab)

**SQL Lab:** Menu superior → **SQL** → **SQL Lab**

#### **Métricas Consolidadas (Últimos 30 dias):**

```sql
SELECT 
    data,
    SUM(spend) as total_spend,
    SUM(reach) as total_reach,
    SUM(new_followers) as total_followers,
    ROUND(AVG(ctr), 2) as avg_ctr,
    ROUND(
        CASE 
            WHEN SUM(new_followers) > 0 
            THEN SUM(spend) / SUM(new_followers) 
            ELSE 0 
        END, 
    2) as cost_per_follower
FROM daily_metrics
WHERE data >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY data
ORDER BY data DESC;
```

#### **Comparação Meta Ads vs Google Ads:**

```sql
SELECT 
    source,
    SUM(spend) as total_invest,
    SUM(new_followers) as total_followers,
    ROUND(SUM(spend) / NULLIF(SUM(new_followers), 0), 2) as cost_per_follower,
    ROUND(AVG(ctr), 2) as avg_ctr,
    COUNT(*) as days_active
FROM daily_metrics
WHERE source IN ('meta_ads', 'google_ads')
  AND data >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY source
ORDER BY total_invest DESC;
```

#### **Top 5 Dias de Melhor Performance:**

```sql
SELECT 
    data,
    source,
    new_followers,
    cost_per_follower,
    ctr,
    notes
FROM daily_metrics
WHERE new_followers > 0
ORDER BY cost_per_follower ASC
LIMIT 5;
```

#### **Tendência de CTR (Últimos 14 dias):**

```sql
SELECT 
    data,
    source,
    ctr,
    AVG(ctr) OVER (
        PARTITION BY source 
        ORDER BY data 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as ctr_moving_avg_7d
FROM daily_metrics
WHERE data >= CURRENT_DATE - INTERVAL '14 days'
  AND ctr IS NOT NULL
ORDER BY data DESC, source;
```

---

## 🎨 Personalização

### **Trocar Senha Admin:**

1. Menu superior direito → **Settings** → **User Settings**
2. **Security** → **Change Password**

### **Tema Escuro:**

1. Menu superior direito → **Settings** → **Preferences**
2. **Theme:** Dark

### **Timezone:**

```bash
docker exec -it superset sh -c "
export SUPERSET_TIMEZONE='America/Sao_Paulo'
"
```

---

## 🔒 Segurança

### **Configurações Recomendadas:**

1. **Trocar Secret Key:**
   - Editar `docker-compose.superset.yml`
   - Gerar novo: `openssl rand -base64 42`

2. **Criar Usuários:**
   - Settings → **List Users** → **"+ User"**
   - Roles: `Alpha` (read-only), `Admin` (full access)

3. **Não expor porta publicamente:**
   - Manter `localhost:8088`
   - Usar VPN ou SSH tunnel para acesso remoto

---

## 📊 Exemplos de Dashboards

### **KPIs Principais (Cards):**

| Métrica | Query | Threshold |
|---------|-------|-----------|
| **Custo/Seguidor** | `AVG(cost_per_follower)` | < R$ 1,30 (verde) |
| **CTR Médio** | `AVG(ctr)` | > 1,5% (verde) |
| **Gasto Diário** | `SUM(spend) / 7` | R$ 40,00 target |
| **Novos Seguidores** | `SUM(new_followers)` | +200/semana target |

### **Gráfico de Tendência:**

```sql
-- Meta vs Realidade (Seguidores)
WITH daily_goal AS (
    SELECT 
        generate_series(
            '2025-10-11'::date,
            '2025-11-08'::date,
            '1 day'::interval
        )::date as data,
        36 as meta_diaria -- 1000 seguidores / 28 dias
)
SELECT 
    dg.data,
    dg.meta_diaria,
    COALESCE(SUM(dm.new_followers), 0) as followers_real,
    SUM(COALESCE(dm.new_followers, 0)) OVER (ORDER BY dg.data) as followers_acumulado,
    SUM(dg.meta_diaria) OVER (ORDER BY dg.data) as meta_acumulada
FROM daily_goal dg
LEFT JOIN daily_metrics dm ON dg.data = dm.data
GROUP BY dg.data, dg.meta_diaria
ORDER BY dg.data;
```

---

## 🛠️ Troubleshooting

### **Superset não inicia:**
```bash
docker logs superset
# Ver erros
```

### **Não conecta ao Supabase:**
- Verificar password no connection string
- Testar conexão Supabase direto: `psql "postgresql://..."`
- Verificar firewall/porta 5432

### **Charts não carregam:**
- Verificar SQL no SQL Lab primeiro
- Ver logs: Settings → **Logs**

### **Performance lenta:**
- Criar índices no Supabase
- Limitar período de dados (últimos 90 dias)
- Usar cache do Superset (Settings → **Cache**)

---

## 📚 Recursos

- **Dashboard Exemplo:** Importar de https://superset.apache.org/docs/using-superset/creating-your-first-dashboard
- **Chart Gallery:** https://superset.apache.org/docs/using-superset/exploring-data
- **SQL Lab Guide:** https://superset.apache.org/docs/using-superset/sql-lab

---

## ✅ Checklist de Setup

- [ ] Docker Superset instalado e rodando
- [ ] Acesso ao http://localhost:8088 funcionando
- [ ] Conectado ao Supabase (PostgreSQL)
- [ ] Datasets criados (daily_metrics, views)
- [ ] Dashboard "Marketing Overview" criado
- [ ] 4-6 charts adicionados ao dashboard
- [ ] Senha admin alterada
- [ ] Usuários adicionais criados (opcional)

---

**🎉 Apache Superset configurado! Dashboards prontos para visualização.**

**Próximo:** Criar workflows n8n para alimentar os dados

