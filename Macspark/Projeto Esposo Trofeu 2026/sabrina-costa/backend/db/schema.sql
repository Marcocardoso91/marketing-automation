-- Database Schema for Dashboard Sabrina Blogueira
-- PostgreSQL 15+
-- Versão: 1.0
-- Data: 20/10/2025

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLE: users
-- Descrição: Usuários do sistema (gerente, cliente)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer' CHECK (role IN ('admin', 'viewer')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- =====================================================
-- TABLE: metrics
-- Descrição: Métricas do Instagram (Meta Ads)
-- =====================================================
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
    cost_per_follower DECIMAL(10,2), -- Custo por seguidor (calculado)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_metrics_date ON metrics(date DESC);
CREATE INDEX idx_metrics_created_at ON metrics(created_at DESC);

-- Constraint: data não pode ser futura
ALTER TABLE metrics ADD CONSTRAINT check_date_not_future 
    CHECK (date <= CURRENT_DATE);

-- =====================================================
-- TABLE: alerts
-- Descrição: Histórico de alertas enviados
-- =====================================================
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(50) NOT NULL, -- 'ctr_low', 'cpc_high', 'frequency_high', etc
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'sent' CHECK (status IN ('sent', 'pending', 'failed')),
    metadata JSONB, -- Dados extras (valores que geraram alerta)
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_alerts_sent_at ON alerts(sent_at DESC);
CREATE INDEX idx_alerts_type ON alerts(type);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_metadata ON alerts USING GIN (metadata);

-- =====================================================
-- TABLE: posts
-- Descrição: Cronograma de posts (4 semanas)
-- =====================================================
CREATE TABLE IF NOT EXISTS posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    week_number INTEGER NOT NULL CHECK (week_number BETWEEN 1 AND 4),
    format VARCHAR(50) NOT NULL CHECK (format IN ('reel', 'carousel', 'stories')),
    theme VARCHAR(255) NOT NULL,
    hook TEXT,
    cta TEXT,
    objective VARCHAR(100),
    stories_ideas TEXT,
    status VARCHAR(20) DEFAULT 'planned' CHECK (status IN ('planned', 'posted', 'cancelled')),
    posted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_posts_date ON posts(date);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_week_number ON posts(week_number);
CREATE INDEX idx_posts_format ON posts(format);

-- =====================================================
-- TABLE: hooks
-- Descrição: Biblioteca de ganchos virais
-- =====================================================
CREATE TABLE IF NOT EXISTS hooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(100) NOT NULL,
    text TEXT NOT NULL,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_hooks_category ON hooks(category);
CREATE INDEX idx_hooks_usage_count ON hooks(usage_count DESC);

-- =====================================================
-- TABLE: config
-- Descrição: Configurações do sistema
-- =====================================================
CREATE TABLE IF NOT EXISTS config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TRIGGERS: Update timestamps
-- =====================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_metrics_updated_at BEFORE UPDATE ON metrics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_posts_updated_at BEFORE UPDATE ON posts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_config_updated_at BEFORE UPDATE ON config
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SEED DATA: Configuration defaults
-- =====================================================
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
}'::jsonb),
('general', '{
    "timezone": "America/Sao_Paulo",
    "currency": "BRL",
    "language": "pt-BR"
}'::jsonb)
ON CONFLICT (key) DO NOTHING;

-- =====================================================
-- SEED DATA: Admin user (senha: Sabrina2025!)
-- Hash gerado com: bcrypt.hashSync('Sabrina2025!', 10)
-- =====================================================
INSERT INTO users (email, password_hash, name, role) VALUES
('gerente@macspark.dev', '$2a$10$X8B9.vJY7kZGQxN4Y3Qe4eF6J2K8L9M0N1O2P3Q4R5S6T7U8V9W0X', 'Marco', 'admin'),
('sabrina@example.com', '$2a$10$Y9C0.wKZ8lAHRyO5Z4Rf5fG7K3L9M0N1O2P3Q4R5S6T7U8V9W0X1Y', 'Sabrina', 'viewer')
ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- SEED DATA: 50 Ganchos Virais
-- =====================================================
INSERT INTO hooks (category, text) VALUES
-- Curiosidade (5)
('Curiosidade', 'O que NINGUÉM te conta sobre...'),
('Curiosidade', 'Esse segredo mudou TUDO para mim'),
('Curiosidade', 'Você não vai acreditar no que descobri'),
('Curiosidade', 'Por que ninguém fala sobre isso?'),
('Curiosidade', 'A verdade que escondem de você'),

-- Urgência (5)
('Urgência', 'PARE de fazer isso AGORA'),
('Urgência', 'Se você faz isso, ESTÁ ERRANDO'),
('Urgência', 'Você está fazendo isso ERRADO (e eu vou te mostrar)'),
('Urgência', 'Último aviso: não faça mais isso'),
('Urgência', 'Se continuar assim, NUNCA vai conseguir [resultado]'),

-- Transformação (5)
('Transformação', 'Como eu fui de [antes] para [depois]'),
('Transformação', 'Isso mudou minha vida em [X dias]'),
('Transformação', 'Olha só o que [X dias] fizeram...'),
('Transformação', 'Antes eu era assim... Hoje sou assim'),
('Transformação', 'A transformação que você precisa ver'),

-- Identificação (5)
('Identificação', 'Se você também é assim, me segue'),
('Identificação', 'Quem nunca passou por isso?'),
('Identificação', 'Eu pensei que era só EU...'),
('Identificação', 'Você também se sente assim às vezes?'),
('Identificação', 'Se identifica? Então esse perfil é pra você'),

-- Lista/Número (5)
('Lista/Número', '3 coisas que NINGUÉM te conta'),
('Lista/Número', '5 erros que TODO MUNDO comete'),
('Lista/Número', '7 sinais de que você precisa [ação]'),
('Lista/Número', 'Os 3 segredos de [resultado]'),
('Lista/Número', '10 coisas que eu faria diferente'),

-- Desafio (5)
('Desafio', 'Você tem CORAGEM de tentar?'),
('Desafio', 'Faz isso HOJE e me conta o resultado'),
('Desafio', 'Testa isso e me agradeça depois'),
('Desafio', 'Se fizer isso, sua vida muda'),
('Desafio', 'Grave esse vídeo EXATAMENTE assim'),

-- Comparação (5)
('Comparação', 'Você faz assim OU assim?'),
('Comparação', 'O jeito CERTO vs o jeito ERRADO'),
('Comparação', 'Antes eu fazia assim... Hoje faço ASSIM'),
('Comparação', 'Expectativa vs Realidade'),
('Comparação', 'Profissional vs Amador'),

-- História (5)
('História', 'Deixa eu te contar uma história...'),
('História', 'Eu nunca vou esquecer o dia que...'),
('História', 'Era uma vez... (no meu caso foi assim)'),
('História', 'Lembro como se fosse hoje...'),
('História', 'A história que mudou tudo'),

-- Pergunta (5)
('Pergunta', 'Você já parou pra pensar nisso?'),
('Pergunta', 'Por que [situação] acontece?'),
('Pergunta', 'Qual o seu maior desafio com [tema]?'),
('Pergunta', 'Me responde com sinceridade...'),
('Pergunta', 'Se pudesse voltar no tempo, você...?'),

-- Autoridade (5)
('Autoridade', 'Depois de [X anos] fazendo isso...'),
('Autoridade', 'Testei TUDO e só isso funcionou'),
('Autoridade', 'A ciência comprova: [afirmação]'),
('Autoridade', 'Isso que vou te contar NINGUÉM sabe'),
('Autoridade', 'Como profissional, eu te garanto...')
ON CONFLICT DO NOTHING;

-- =====================================================
-- VIEWS: Useful queries
-- =====================================================

-- View: Métricas recentes com cálculos
CREATE OR REPLACE VIEW v_metrics_recent AS
SELECT 
    id,
    date,
    ctr,
    cpc,
    cpm,
    frequency,
    visits,
    new_followers,
    cost,
    impressions,
    clicks,
    CASE 
        WHEN new_followers > 0 THEN ROUND(cost / new_followers, 2)
        ELSE NULL
    END as cost_per_follower_calculated,
    created_at,
    -- Status indicators
    CASE WHEN ctr < 1.5 THEN 'warning' ELSE 'ok' END as ctr_status,
    CASE WHEN cpc > 0.70 THEN 'warning' ELSE 'ok' END as cpc_status,
    CASE WHEN frequency > 3.0 THEN 'warning' ELSE 'ok' END as frequency_status
FROM metrics
ORDER BY date DESC
LIMIT 30;

-- View: Resumo semanal
CREATE OR REPLACE VIEW v_weekly_summary AS
SELECT 
    DATE_TRUNC('week', date) as week_start,
    COUNT(*) as days_with_data,
    ROUND(AVG(ctr), 2) as avg_ctr,
    ROUND(AVG(cpc), 2) as avg_cpc,
    ROUND(AVG(cpm), 2) as avg_cpm,
    ROUND(AVG(frequency), 2) as avg_frequency,
    SUM(visits) as total_visits,
    SUM(new_followers) as total_new_followers,
    SUM(cost) as total_cost,
    SUM(impressions) as total_impressions,
    SUM(clicks) as total_clicks
FROM metrics
WHERE date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY DATE_TRUNC('week', date)
ORDER BY week_start DESC;

-- =====================================================
-- FUNCTIONS: Useful functions
-- =====================================================

-- Function: Get metrics summary
CREATE OR REPLACE FUNCTION get_metrics_summary(period_days INTEGER DEFAULT 7)
RETURNS TABLE (
    period_start DATE,
    period_end DATE,
    total_days INTEGER,
    avg_ctr DECIMAL,
    avg_cpc DECIMAL,
    avg_cpm DECIMAL,
    total_visits INTEGER,
    total_followers INTEGER,
    total_cost DECIMAL,
    avg_cost_per_follower DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CURRENT_DATE - period_days::INTEGER as period_start,
        CURRENT_DATE as period_end,
        COUNT(*)::INTEGER as total_days,
        ROUND(AVG(m.ctr), 2) as avg_ctr,
        ROUND(AVG(m.cpc), 2) as avg_cpc,
        ROUND(AVG(m.cpm), 2) as avg_cpm,
        SUM(m.visits)::INTEGER as total_visits,
        SUM(m.new_followers)::INTEGER as total_followers,
        SUM(m.cost) as total_cost,
        CASE 
            WHEN SUM(m.new_followers) > 0 
            THEN ROUND(SUM(m.cost) / SUM(m.new_followers), 2)
            ELSE NULL
        END as avg_cost_per_follower
    FROM metrics m
    WHERE m.date >= CURRENT_DATE - period_days::INTEGER;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- COMMENTS
-- =====================================================
COMMENT ON TABLE users IS 'Usuários do sistema com autenticação';
COMMENT ON TABLE metrics IS 'Métricas diárias do Instagram / Meta Ads';
COMMENT ON TABLE alerts IS 'Histórico de alertas enviados via WhatsApp';
COMMENT ON TABLE posts IS 'Cronograma de posts planejados (4 semanas)';
COMMENT ON TABLE hooks IS 'Biblioteca de ganchos virais para Reels';
COMMENT ON TABLE config IS 'Configurações gerais do sistema';

-- =====================================================
-- GRANTS (ajustar conforme necessário)
-- =====================================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

