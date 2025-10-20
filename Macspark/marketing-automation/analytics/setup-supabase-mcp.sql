-- ============================================
-- CONFIGURAÇÃO SUPABASE VIA MCP
-- Projeto: Agente Facebook / Projeto Sabrina
-- Data: 18/10/2025
-- ============================================

-- 1. CRIAR TABELA PRINCIPAL: daily_metrics
CREATE TABLE IF NOT EXISTS daily_metrics (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    source VARCHAR(50) NOT NULL,
    
    -- Métricas básicas
    spend DECIMAL(10,2) DEFAULT 0,
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    
    -- Métricas calculadas
    ctr DECIMAL(5,2) DEFAULT 0,
    cpc DECIMAL(10,4) DEFAULT 0,
    cpm DECIMAL(10,2) DEFAULT 0,
    frequency DECIMAL(5,2) DEFAULT 0,
    
    -- Conversões e seguidores
    conversions INTEGER DEFAULT 0,
    new_followers INTEGER DEFAULT 0,
    cost_per_conversion DECIMAL(10,2) DEFAULT 0,
    cost_per_follower DECIMAL(10,2) DEFAULT 0,
    
    -- Métricas específicas por fonte
    views INTEGER DEFAULT 0, -- YouTube
    subscribers_gained INTEGER DEFAULT 0, -- YouTube
    sessions INTEGER DEFAULT 0, -- Google Analytics
    users INTEGER DEFAULT 0, -- Google Analytics
    bounce_rate DECIMAL(5,2) DEFAULT 0, -- Google Analytics
    
    -- Metadados
    notes TEXT,
    raw_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(data, source)
);

-- 2. CRIAR ÍNDICES PARA PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_daily_metrics_data ON daily_metrics(data);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_source ON daily_metrics(source);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_data_source ON daily_metrics(data, source);

-- 3. CRIAR VIEW: metrics_consolidated (consolidação diária)
CREATE OR REPLACE VIEW metrics_consolidated AS
SELECT 
    data,
    COUNT(*) as sources_count,
    SUM(spend) as total_spend,
    SUM(reach) as total_reach,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks,
    SUM(new_followers) as total_new_followers,
    SUM(conversions) as total_conversions,
    
    -- Métricas calculadas
    CASE 
        WHEN SUM(impressions) > 0 THEN (SUM(clicks)::DECIMAL / SUM(impressions)) * 100 
        ELSE 0 
    END as avg_ctr,
    
    CASE 
        WHEN SUM(clicks) > 0 THEN SUM(spend) / SUM(clicks) 
        ELSE 0 
    END as avg_cpc,
    
    CASE 
        WHEN SUM(impressions) > 0 THEN (SUM(spend) / SUM(impressions)) * 1000 
        ELSE 0 
    END as avg_cpm,
    
    CASE 
        WHEN SUM(new_followers) > 0 THEN SUM(spend) / SUM(new_followers) 
        ELSE 0 
    END as avg_cost_per_follower,
    
    -- Performance por fonte
    STRING_AGG(
        source || ': R$' || spend::TEXT || ' (' || new_followers::TEXT || ' seguidores)',
        ', '
    ) as performance_by_source,
    
    created_at
FROM daily_metrics
GROUP BY data, created_at
ORDER BY data DESC;

-- 4. CRIAR VIEW: performance_by_source (análise por fonte)
CREATE OR REPLACE VIEW performance_by_source AS
SELECT 
    source,
    COUNT(*) as days_tracked,
    AVG(spend) as avg_daily_spend,
    AVG(new_followers) as avg_daily_followers,
    AVG(ctr) as avg_ctr,
    AVG(cpc) as avg_cpc,
    AVG(cost_per_follower) as avg_cost_per_follower,
    SUM(spend) as total_spend,
    SUM(new_followers) as total_followers,
    
    -- ROI calculado
    CASE 
        WHEN SUM(spend) > 0 AND SUM(new_followers) > 0 
        THEN (SUM(new_followers) * 1.30) / SUM(spend) -- Assumindo R$ 1,30 por seguidor
        ELSE 0 
    END as estimated_roi,
    
    MAX(data) as last_update
FROM daily_metrics
WHERE spend > 0 OR new_followers > 0
GROUP BY source
ORDER BY total_followers DESC;

-- 5. CRIAR VIEW: weekly_summary (resumo semanal)
CREATE OR REPLACE VIEW weekly_summary AS
SELECT 
    DATE_TRUNC('week', data) as week_start,
    COUNT(DISTINCT data) as days_tracked,
    COUNT(DISTINCT source) as sources_active,
    SUM(spend) as total_spend,
    SUM(new_followers) as total_followers,
    AVG(ctr) as avg_ctr,
    AVG(cost_per_follower) as avg_cost_per_follower,
    
    -- Crescimento semanal
    LAG(SUM(new_followers)) OVER (ORDER BY DATE_TRUNC('week', data)) as prev_week_followers,
    SUM(new_followers) - LAG(SUM(new_followers)) OVER (ORDER BY DATE_TRUNC('week', data)) as followers_growth,
    
    MAX(data) as last_update
FROM daily_metrics
GROUP BY DATE_TRUNC('week', data)
ORDER BY week_start DESC;

-- 6. CRIAR TRIGGER: auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_daily_metrics_updated_at 
    BEFORE UPDATE ON daily_metrics 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- 7. INSERIR DADOS DE TESTE (opcional)
INSERT INTO daily_metrics (
    data, source, spend, reach, impressions, clicks, 
    ctr, cpc, new_followers, cost_per_follower, notes
) VALUES 
(
    CURRENT_DATE - INTERVAL '1 day', 
    'meta_ads', 
    25.50, 
    1250, 
    8500, 
    127, 
    1.49, 
    0.20, 
    19, 
    1.34, 
    'Dados de teste - Meta Ads'
),
(
    CURRENT_DATE - INTERVAL '1 day', 
    'youtube', 
    0.00, 
    450, 
    450, 
    0, 
    0.00, 
    0.00, 
    3, 
    0.00, 
    'Dados de teste - YouTube'
)
ON CONFLICT (data, source) DO NOTHING;

-- 8. CRIAR POLÍTICAS RLS (Row Level Security)
ALTER TABLE daily_metrics ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (para uso interno)
CREATE POLICY "Allow all operations for service role" ON daily_metrics
    FOR ALL USING (true);

-- 9. VERIFICAR ESTRUTURA CRIADA
SELECT 
    'Tabela daily_metrics criada com sucesso!' as status,
    COUNT(*) as total_records
FROM daily_metrics;

SELECT 
    'Views criadas com sucesso!' as status,
    COUNT(*) as view_count
FROM information_schema.views 
WHERE table_schema = 'public' 
AND table_name IN ('metrics_consolidated', 'performance_by_source', 'weekly_summary');
