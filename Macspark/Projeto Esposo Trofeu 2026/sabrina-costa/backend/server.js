/**
 * Express Server - Dashboard Sabrina Costa
 * API REST para gerenciamento de métricas do Instagram
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const { testConnection } = require('./db/connection');

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// =====================================================
// MIDDLEWARE
// =====================================================

// Security headers
app.use(helmet());

// CORS configuration
const corsOptions = {
    origin: process.env.CORS_ORIGIN ? process.env.CORS_ORIGIN.split(',') : ['http://localhost:3000'],
    credentials: true,
    optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Body parsers
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(express.text({ type: 'text/csv', limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 60000, // 1 minute
    max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100,
    message: { success: false, error: 'Muitas requisições. Tente novamente em 1 minuto.' },
    standardHeaders: true,
    legacyHeaders: false,
});
app.use('/api/', limiter);

// Request logging
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    next();
});

// =====================================================
// ROUTES
// =====================================================

// Import route handlers
const authRoutes = require('./api/auth');
const metricsRoutes = require('./api/metrics');
const webhookRoutes = require('./api/webhook');
const alertsRoutes = require('./api/alerts');
const scheduleRoutes = require('./api/schedule');
const hooksRoutes = require('./api/hooks');
const configRoutes = require('./api/config');

// Health check
app.get('/api/health', (req, res) => {
    res.json({
        success: true,
        status: 'online',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
    });
});

// API routes
app.use('/api/auth', authRoutes);
app.use('/api/metrics', metricsRoutes);
app.use('/api/webhook', webhookRoutes);
app.use('/api/alerts', alertsRoutes);
app.use('/api/schedule', scheduleRoutes);
app.use('/api/hooks', hooksRoutes);
app.use('/api/config', configRoutes);

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint não encontrado',
        path: req.path
    });
});

// Global error handler
app.use((err, req, res, next) => {
    console.error('[ERROR]', err);
    
    res.status(err.status || 500).json({
        success: false,
        error: err.message || 'Erro interno do servidor',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
});

// =====================================================
// START SERVER
// =====================================================

async function startServer() {
    try {
        // Test database connection
        const dbConnected = await testConnection();
        
        if (!dbConnected && process.env.NODE_ENV === 'production') {
            throw new Error('Falha ao conectar ao banco de dados');
        }
        
        // Start listening
        app.listen(PORT, () => {
            console.log('');
            console.log('═══════════════════════════════════════');
            console.log('  🌟 Dashboard Sabrina Costa API');
            console.log('═══════════════════════════════════════');
            console.log(`  📡 Servidor rodando em http://localhost:${PORT}`);
            console.log(`  🗄️  Banco de dados: ${dbConnected ? '✓ Conectado' : '✗ Desconectado'}`);
            console.log(`  🔒 Ambiente: ${process.env.NODE_ENV || 'development'}`);
            console.log('═══════════════════════════════════════');
            console.log('');
            console.log('  📖 Endpoints disponíveis:');
            console.log('     GET  /api/health');
            console.log('     POST /api/auth/login');
            console.log('     GET  /api/metrics');
            console.log('     POST /api/metrics');
            console.log('     POST /api/webhook/metrics');
            console.log('');
        });
        
    } catch (error) {
        console.error('❌ Falha ao iniciar servidor:', error.message);
        process.exit(1);
    }
}

// Start the server
if (require.main === module) {
    startServer();
}

// Export for testing
module.exports = app;

